from tools.evidence import atlas as A
R = A.rows(); S = A.summary(R)
def test_labels_and_rules():
    assert all(r['label'] in 'PFASG' and r['status'] in ('pass', 'tension', 'fail', 'open') for r in R)
    ids = {r['id']: r for r in R}
    assert ids['bbn-li7']['status'] == 'fail' and ids['late-coupling']['status'] == 'fail'          # rule 6: failures kept
    assert all(r['label'] == 'F' for r in R if r['id'].startswith('infl-ns'))                        # n_s is fitted
    assert not any(r.get('headline') and r['label'] != 'P' for r in R)                               # rule 4
    assert sum(1 for r in R if r.get('headline') and r['id'].startswith('late-thread')) == 1         # rule 5
