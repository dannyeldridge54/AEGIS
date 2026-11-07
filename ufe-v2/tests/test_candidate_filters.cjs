const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const html = fs.readFileSync(path.join(__dirname, '..', 'monitor.html'), 'utf8');
const context = vm.createContext({});
const logic = html.slice(html.indexOf('function finiteRecorded('), html.indexOf('function displayCandidates('));
vm.runInContext(logic, context);
const {finiteRecorded, recordedValue, partialUncertaintyUsable, candidateMatches, candidateViewExport} = context;
const row = {
  id:'5853498713190525696', flags:'high_velocity;astrometric_excess', flag_notes:'Follow up',
  catalog_values:{rv:'0', parallax_error:'0', pmra_error:'.2', pmdec_error:'.3', pmra_pmdec_corr:'0'},
  derived_values:{r_lo_geo:'900', r_hi_geo:'1100'}
};
const filters = {query:'', flag:'', rv:'', uncertainty:''};

test('finite input distinguishes missing, invalid and valid zero', () => {
  for (const value of [null, undefined, '', ' ', 'NaN', 'Infinity', true, [], {}]) {
    assert.equal(finiteRecorded(value), false);
  }
  for (const value of [0, '0', '-25.2', 3]) assert.equal(finiteRecorded(value), true);
  assert.equal(recordedValue(0), 0);
  assert.equal(recordedValue(''), '—');
});

test('RV and partial uncertainty filters accept zero, and compose with flags/search', () => {
  assert.equal(partialUncertaintyUsable(row), true);
  assert.equal(candidateMatches(row, {...filters, rv:'available', uncertainty:'usable',
    flag:'high_velocity', query:'585349'}), true);
  assert.equal(candidateMatches(row, {...filters, rv:'missing'}), false);
  assert.equal(candidateMatches(row, {...filters, flag:'distance_mismatch'}), false);
  assert.equal(candidateMatches(row, {...filters, query:'not present'}), false);
});

test('partial uncertainty filters reject invalid ranges and missing legacy inputs', () => {
  for (const change of [{pmra_error:'-1'}, {pmra_pmdec_corr:'1.01'}, {parallax_error:''}]) {
    const bad = {...row, catalog_values:{...row.catalog_values, ...change}};
    assert.equal(partialUncertaintyUsable(bad), false);
    assert.equal(candidateMatches(bad, {...filters, uncertainty:'missing'}), true);
  }
  assert.equal(partialUncertaintyUsable({...row, derived_values:{r_lo_geo:'100', r_hi_geo:'100'}}), false);
  assert.equal(partialUncertaintyUsable({...row, derived_values:{r_lo_geo:'0', r_hi_geo:'100'}}), false);
  assert.equal(candidateMatches({id:'legacy'}, {...filters, rv:'missing', uncertainty:'missing'}), true);
});

test('filtered export preserves IDs, parent scope, provenance and original evidence', () => {
  const data = {generated_utc:'2026-11-05T01:00:00Z', run_id:'fixture', schema_version:4,
    report_version:'3.4', sources:[{sha256:'fixture'}],
    observational_evidence:{candidate_export:{rows:[row,{id:'missing'}],
      row_limit:20000, display_limit:40, truncated:true}}};
  const before = JSON.stringify(data);
  const output = candidateViewExport(data, {...filters, rv:'available'});
  assert.equal(output.rows.length, 1);
  assert.equal(output.rows[0].id, row.id);
  assert.equal(output.report_generated_utc, data.generated_utc);
  assert.equal(output.sources[0].sha256, 'fixture');
  assert.equal(output.parent_export.truncated, true);
  assert.equal(output.parent_export.display_limit, 40);
  assert.equal(output.limitations.length, 3);
  assert.equal(JSON.stringify(data), before);
  assert.equal(candidateViewExport(data, {...filters, query:'no match'}).rows.length, 0);
});

test('complete dashboard script parses and all filter controls are wired', () => {
  for (const match of html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) {
    new vm.Script(match[1]);
  }
  for (const id of ['rv-filter', 'uncertainty-filter', 'export-candidates']) {
    assert.ok(html.includes(`id="${id}"`));
    assert.ok(html.includes(`$('${id}').addEventListener`));
  }
  assert.ok(html.includes('setInterval(loadReport, 60000)'));
});

function browserContext() {
  const nodes = new Map();
  function node(id) {
    if (!nodes.has(id)) {
      const value = {textContent:'',value:'',children:[],appendChild(child) {this.children.push(child);}};
      Object.defineProperty(value,'innerHTML',{
        get() {return this.content || '';},
        set(content) {this.content=content;this.children=[];}
      });
      nodes.set(id,value);
    }
    return nodes.get(id);
  }
  return vm.createContext({$:node, reportData:null, URL,
    esc:value => String(value), fmt:value => String(value), ratio:value => String(value),
    document:{createElement:() => ({})}, compareSnapshots:() => {}, displayCandidates:() => {}});
}

test('old reports clear research labels and repeated refresh does not duplicate flag options', () => {
  const browser = browserContext();
  vm.runInContext(logic, browser);
  browser.displayCandidates = () => {};
  vm.runInContext(html.slice(html.indexOf('function showReport('),html.indexOf('async function updateLive(')), browser);
  const data = {generated_utc:'2026-11-05T01:00:00Z', observational_evidence:{},
    anomaly_definitions_and_controls:{criteria:{high_velocity:{rule:'test',definition:'test',confirm:'test'}}}};
  browser.$('research-channels').innerHTML = 'old channels';
  browser.showReport(data);
  browser.$('flag-filter').value='high_velocity';
  browser.showReport(data);
  assert.equal(browser.$('flag-filter').children.length,1);
  assert.equal(browser.$('flag-filter').value,'high_velocity');
  assert.match(browser.$('research-channels').innerHTML,/no research-channel/);
  browser.showReport({...data,anomaly_definitions_and_controls:{criteria:{}}});
  assert.equal(browser.$('flag-filter').value,'');
});

test('HTTP and malformed report failures disable stale candidate exports and expose the error', async () => {
  for (const mode of ['http','json','render']) {
    const browser = browserContext();
    browser.reportData={old:true};
    browser.displayResearchChannels = () => {};
    browser.showReport = () => {throw new Error('Invalid report shape');};
    browser.fetch=async () => ({ok:mode !== 'http',status:503,
      json:async () => {
        if(mode==='json')throw new Error('Malformed JSON');
        return {};
      }});
    vm.runInContext(html.slice(html.indexOf('async function loadReport('),html.indexOf("$('candidate-search').addEventListener")), browser);
    await browser.loadReport();
    assert.equal(browser.reportData,null);
    assert.match(browser.$('candidate-limit').textContent,/export disabled/);
    assert.match(browser.$('report-status').textContent,/503|Malformed JSON|Invalid report shape/);
  }
});

test('successful refresh passes the new snapshot through', async () => {
  const browser=browserContext();
  const data={generated_utc:'new'};
  browser.fetch=async () => ({ok:true,json:async () => data});
  browser.showReport=value => {browser.reportData=value;};
  vm.runInContext(html.slice(html.indexOf('async function loadReport('),html.indexOf("$('candidate-search').addEventListener")), browser);
  await browser.loadReport();
  assert.equal(browser.reportData,data);
});

test('rendered candidate cells preserve numeric zero in derived values', () => {
  const browser = browserContext();
  vm.runInContext(logic, browser);
  vm.runInContext(html.slice(html.indexOf('function displayCandidates('), html.indexOf('const map = {')), browser);
  browser.reportData = {observational_evidence:{candidate_export:{rows:[{
    ...row, derived_values:{dist_bj_pc:0, dist_plx_pc:0, vtan_kms:0, r_lo_geo:0, r_hi_geo:1}
  }]}}};
  browser.displayCandidates();
  assert.ok(browser.$('candidate-rows').innerHTML.includes(
    '<td class="num">0</td><td class="num">0</td>'));
  assert.match(browser.$('candidate-rows').innerHTML, /BJ 16–84%=0–1 pc/);
});

test('missing candidate evidence disables export instead of presenting a zero-result download', () => {
  const browser = browserContext();
  vm.runInContext(logic, browser);
  vm.runInContext(html.slice(html.indexOf('function displayCandidates('), html.indexOf('const map = {')), browser);
  browser.reportData = {observational_evidence:{candidate_export:{status:'missing_not_zero_candidates'}}};
  browser.displayCandidates();
  assert.equal(browser.$('export-candidates').disabled, true);
  browser.reportData.observational_evidence.candidate_export = {status:'available',rows:[]};
  browser.displayCandidates();
  assert.equal(browser.$('export-candidates').disabled, false);
});

test('live status distinguishes missing counts from zero and clears stale values on failure', async () => {
  const browser = browserContext();
  vm.runInContext(logic, browser);
  vm.runInContext(html.slice(html.indexOf('async function updateLive('), html.indexOf('async function loadReport(')), browser);
  for (const value of [null, '', false, 0, '0']) {
    browser.fetch = async () => ({ok:true,json:async () => ({scan:{stars:value}})});
    await browser.updateLive();
    assert.equal(browser.$('live-stars').textContent, value === 0 || value === '0' ? '0' : '—');
  }
  browser.$('live-flag-summary').innerHTML = 'old flags';
  browser.fetch = async () => ({ok:false,status:503});
  await browser.updateLive();
  assert.equal(browser.$('live-stars').textContent, '—');
  assert.equal(browser.$('live-patches').textContent, '—');
  assert.equal(browser.$('live-active').textContent, 'Unavailable');
  assert.match(browser.$('live-checked').textContent, /HTTP 503/);
  assert.match(browser.$('live-flag-summary').innerHTML, /unavailable/);
});

const liveHtml = fs.readFileSync(path.join(__dirname, '..', 'live.html'), 'utf8');
test('livestream avoids damaged historical results and unsupported companion interpretation', () => {
  for (const match of liveHtml.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/g)) new vm.Script(match[1]);
  assert.equal(liveHtml.includes('SCI.result_lines.map'), false);
  assert.equal(liveHtml.includes('SCI.next.map'), false);
  assert.equal(liveHtml.includes('many may hide unseen companions'), false);
  assert.ok(liveHtml.includes('not yet derived from the microscopic torsion action'));
});

test('livestream HTTP or malformed-status failures mark stale telemetry unavailable', async () => {
  for (const mode of ['http','shape']) {
    const browser = browserContext();
    browser.STATUS = {state:'scanning',scan:{stars:123}};
    browser.fetch = async () => ({ok:mode !== 'http',status:503,json:async () => ({})});
    vm.runInContext(liveHtml.slice(liveHtml.indexOf('async function getStatus()'), liveHtml.indexOf('async function getShells()')), browser);
    await browser.getStatus();
    assert.equal(browser.STATUS.state, 'unavailable');
    assert.equal(browser.$('s-stars').textContent, 'Unavailable');
    assert.match(browser.$('s-rate').textContent, /HTTP 503|Invalid live status/);
    assert.match(browser.$('tick').textContent, /not current/);
  }
});
