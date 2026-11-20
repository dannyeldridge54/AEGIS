/* Sarah's Sky — Inner Work: daily guidance, archetypes, chakras, I Ching, runes, numerology and a breathing guide.
   Self-help and esoteric traditions — not astronomy. The sky beneath (Sun, Moon) is real & computed (astronomy-engine).
   All interpretive text is original. Everything stays on the device: no accounts, no tracking. */
(function () {
  var A = window.Astronomy;
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); };
  var norm = function (x) { x %= 360; return x < 0 ? x + 360 : x; };
  var SIGNS = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
  var SG = ['♈︎','♉︎','♊︎','♋︎','♌︎','♍︎','♎︎','♏︎','♐︎','♑︎','♒︎','♓︎'];
  var ELEM = ['Fire','Earth','Air','Water'];
  // secure random for divination; falls back to Math.random only if crypto is missing
  function rnd(n) { try { var a = new Uint32Array(1); (window.crypto || window.msCrypto).getRandomValues(a); return a[0] % n; } catch (e) { return Math.floor(Math.random() * n); } }
  // deterministic hash for "today" content so it is stable through the day
  function seed(str) { var h = 2166136261; for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function pick(arr, s) { return arr[(((s >>> 0) % arr.length) + arr.length) % arr.length]; }

  /* ===================== 1. SKY ARCHETYPES (zodiac) ===================== */
  var ARCH = [
    ['The Pioneer', 'Fire', 'You begin. Where others hesitate, you move — courage is your first language.', 'Gift: initiative, honesty, nerve. Shadow: impatience, picking fights. Growth: finish what you start, and let others catch up.', 'I have the courage to begin.'],
    ['The Builder', 'Earth', 'You make things real and lasting. Comfort, loyalty and the slow growing of worth are yours.', 'Gift: steadiness, patience, devotion. Shadow: stubbornness, clinging. Growth: loosen your grip and let the new in.', 'I am steady, and I am enough.'],
    ['The Messenger', 'Air', 'You connect ideas and people. Curiosity keeps you young and your words carry far.', 'Gift: wit, adaptability, learning. Shadow: scattered, restless, surface-deep. Growth: choose one thing and go deep.', 'My mind is clear and my words are kind.'],
    ['The Nurturer', 'Water', 'You feel the room and tend what is tender. Home is something you carry, not just a place.', 'Gift: empathy, memory, care. Shadow: moodiness, holding on, self-protection. Growth: let yourself be held too.', 'I give care freely and receive it gladly.'],
    ['The Sovereign', 'Fire', 'You shine and you lead from the heart. Warmth, play and creation are your element.', 'Gift: generosity, confidence, joy. Shadow: pride, needing applause. Growth: let love, not the spotlight, be the point.', 'I shine, and I let others shine.'],
    ['The Craftsperson', 'Earth', 'You refine and serve. In the details nobody notices, you quietly make the world work.', 'Gift: skill, devotion, usefulness. Shadow: worry, harsh self-judgement. Growth: "good enough" is often perfect.', 'I do my part well, and I am gentle with myself.'],
    ['The Harmoniser', 'Air', 'You seek balance, beauty and fairness. Relationship is the art you were born to.', 'Gift: grace, diplomacy, taste. Shadow: indecision, people-pleasing. Growth: your own "no" is also beautiful.', 'I choose peace that includes me.'],
    ['The Alchemist', 'Water', 'You go to the depths and come back changed. Nothing stays hidden from you for long.', 'Gift: intensity, loyalty, insight. Shadow: control, suspicion, grudges. Growth: trust, and let what is done be done.', 'I release what I cannot keep, and I am reborn.'],
    ['The Seeker', 'Fire', 'You chase meaning over the next horizon. Freedom and truth are your north star.', 'Gift: optimism, vision, honesty. Shadow: restlessness, tactlessness, escape. Growth: the journey is also here, now.', 'I follow my truth with an open heart.'],
    ['The Mountain', 'Earth', 'You climb, patiently, toward something that lasts. Responsibility sits easily on you.', 'Gift: discipline, integrity, endurance. Shadow: coldness, overwork, fear of failing. Growth: you are worthy before the summit.', 'I build a life of meaning, one honest step at a time.'],
    ['The Visionary', 'Air', 'You see the future and the whole. The strange and the fair both call to you.', 'Gift: originality, friendship, principle. Shadow: detachment, stubborn theories. Growth: come down and be among people.', 'I am free, and I belong.'],
    ['The Mystic', 'Water', 'You dissolve the line between self and world. Compassion and imagination flow through you.', 'Gift: tenderness, artistry, faith. Shadow: escapism, blurred edges, martyrdom. Growth: dreams need a shore to land on.', 'I am open, and I keep myself whole.']
  ];

  /* ===================== 2. THE TWELVE INNER ARCHETYPES (Jungian) ===================== */
  var JUNG = [
    ['The Innocent', 'Longs for safety and simple goodness; trusts that life is kind. At its best, faith and optimism; at its edge, denial.'],
    ['The Everyperson', 'Wants to belong and be real with others; down-to-earth and unpretentious. Gift: empathy. Edge: losing yourself to fit in.'],
    ['The Hero', 'Rises to the challenge and proves worth through courage. Gift: mastery, grit. Edge: everything becomes a battle.'],
    ['The Caregiver', 'Protects and nourishes others. Gift: generosity, compassion. Edge: martyrdom, giving past empty.'],
    ['The Explorer', 'Seeks freedom and a truer life beyond the fence. Gift: authenticity. Edge: never arriving, never belonging.'],
    ['The Rebel', 'Overturns what no longer works. Gift: courage to change. Edge: destruction for its own sake.'],
    ['The Lover', 'Seeks intimacy, beauty and connection. Gift: devotion, passion. Edge: losing identity in the beloved.'],
    ['The Creator', 'Makes something new and meaningful. Gift: imagination, craft. Edge: perfectionism that never ships.'],
    ['The Jester', 'Lives in the now and lightens the load. Gift: joy, truth told sideways. Edge: avoiding depth with a joke.'],
    ['The Sage', 'Seeks truth and understanding. Gift: wisdom, clarity. Edge: analysis that never acts.'],
    ['The Magician', 'Transforms reality and makes dreams happen. Gift: vision, healing. Edge: manipulation, using power to control.'],
    ['The Ruler', 'Creates order and takes responsibility. Gift: leadership, stewardship. Edge: control, fear of chaos.']
  ];

  /* ===================== 3. CHAKRAS ===================== */
  var CHAK = [
    ['Root', 'Muladhara', '#e2444a', 'Earth', 'LAM', 'base of the spine', 'Safety, belonging, the body, "I am here and I have enough."', 'Balanced: grounded, calm, secure. Blocked: anxious, scattered, never safe. Overactive: rigid, hoarding, stuck.', 'Stand barefoot; feel your weight; slow breaths into the belly; name three things that keep you safe.'],
    ['Sacral', 'Svadhisthana', '#f08a3c', 'Water', 'VAM', 'below the navel', 'Feeling, pleasure, creativity, "I allow myself to feel and create."', 'Balanced: flowing, playful, alive. Blocked: numb, guilty, dry. Overactive: overwhelmed, driven by craving.', 'Move your hips; let water run over your hands; make something with no goal; ask what you actually want.'],
    ['Solar Plexus', 'Manipura', '#f4c542', 'Fire', 'RAM', 'upper belly', 'Will, confidence, power, "I can act and I can choose."', 'Balanced: capable, warm, self-assured. Blocked: timid, doormat, powerless. Overactive: domineering, forceful.', 'Set one small boundary today; do one thing you said you would; breathe into the core and feel the ember.'],
    ['Heart', 'Anahata', '#4caf6d', 'Air', 'YAM', 'centre of the chest', 'Love, compassion, forgiveness, "I give and receive love freely."', 'Balanced: open, warm, kind to self. Blocked: lonely, defended, bitter. Overactive: self-sacrificing, no boundaries.', 'Hand on heart, three slow breaths; forgive yourself one thing; tell someone what you appreciate.'],
    ['Throat', 'Vishuddha', '#4aa3df', 'Ether', 'HAM', 'the throat', 'Truth, voice, expression, "I speak and live my truth."', 'Balanced: honest, clear, heard. Blocked: silent, unexpressed, hoarse. Overactive: talks over, cannot listen.', 'Say the true thing kindly; hum or sing; write the sentence you have been swallowing.'],
    ['Third Eye', 'Ajna', '#5a5ad8', 'Light', 'OM', 'between the brows', 'Insight, intuition, vision, "I see clearly and I trust what I know."', 'Balanced: wise, perceptive, calm-minded. Blocked: foggy, cynical, cut off from intuition. Overactive: lost in fantasy.', 'Soften your gaze; sit with one question and do not answer it; notice your first instinct and honour it.'],
    ['Crown', 'Sahasrara', '#9b59d0', 'Thought', 'silence', 'top of the head', 'Connection, meaning, the whole, "I am part of something larger."', 'Balanced: open, trusting, at peace. Blocked: cynical, disconnected, meaningless. Overactive: ungrounded, spiritual bypass.', 'Sit in silence a minute; look up at the sky; let one worry go to something bigger than you.']
  ];

  /* ===================== 4. RUNES — Elder Futhark ===================== */
  // [symbol, name, keyword, upright, reversed]  (reversed '' = symmetric rune, no reversal)
  var RUNE = [
    ['ᚠ','Fehu','Wealth','Earned abundance, energy flowing in, prosperity you can share. A good start.','Loss, scattered resources, holding too tight. Mind where your energy goes.'],
    ['ᚢ','Uruz','Strength','Raw vitality, wild health, the will to push through. Untamed power.','Weakness, misused force, missed chances. Gather yourself before you act.'],
    ['ᚦ','Thurisaz','The Gate','A force to be reckoned with; protection, but also a warning. Pause before the threshold.','Defencelessness, rash action, a door you should not open yet.'],
    ['ᚨ','Ansuz','The Message','A sign, wise counsel, words that matter. Listen for the signal.','Misunderstanding, bad advice, lies. Do not take everything at face value.'],
    ['ᚱ','Raidho','The Journey','Right action, a journey with purpose, things in rhythm. Travel well.','Disruption, a trip gone wrong, being out of step. Reconsider the route.'],
    ['ᚲ','Kenaz','The Torch','Insight, learning, creative fire, seeing in the dark. Light revealed.','Dimming, loss of clarity, a project cooling. Tend the flame.'],
    ['ᚷ','Gebo','The Gift','Partnership, generosity, a fair exchange, union of equals. A gift given freely.',''],
    ['ᚹ','Wunjo','Joy','Harmony, well-being, belonging, a wish fulfilled. Shared gladness.','Delayed joy, discord, going it alone for now. Tend your bonds.'],
    ['ᚺ','Hagalaz','The Hail','Disruption you did not choose, a storm that clears the ground. Weather it.',''],
    ['ᚾ','Nauthiz','Need','Constraint, a hard lesson, patience under pressure. Needs met the slow way.','Deprivation, stubborn resistance, want that gnaws. Face the lack honestly.'],
    ['ᛁ','Isa','Ice','Stillness, a pause, things frozen for now. Wait; do not force.',''],
    ['ᛃ','Jera','The Harvest','Reward in its season, the year turning, patience paying off. You reap what you sowed.',''],
    ['ᛇ','Eihwaz','The Yew','Endurance, a strong backbone, reliable defence. Steady through change.',''],
    ['ᛈ','Perthro','The Cup','Mystery, chance, hidden things, what is being born. Trust the unknown.','Stagnation, secrets kept too long, luck withheld. Let it come to light.'],
    ['ᛉ','Algiz','Protection','A shield, higher help, strong boundaries, instinct that guards you.','Exposure, a boundary down, warning ignored. Protect yourself.'],
    ['ᛊ','Sowilo','The Sun','Wholeness, success, life force, light after dark. Victory and health.',''],
    ['ᛏ','Tiwaz','The Warrior','Honour, justice, courage to do what is right. Stand for something.','Injustice, failing courage, energy draining. Check your cause and your strength.'],
    ['ᛒ','Berkano','Growth','New beginnings, birth, nurturing, quiet becoming. Something tender grows.','Stalled growth, neglect, family trouble. Tend what you are raising.'],
    ['ᛖ','Ehwaz','The Horse','Movement, trust, partnership, steady progress together. Onward, as a team.','Restlessness, a partnership out of sync, feeling stuck. Rebuild trust.'],
    ['ᛗ','Mannaz','The Self','Humanity, your place among others, clear self-knowledge. Know yourself.','Isolation, self-deception, a blind spot. Ask an honest friend.'],
    ['ᛚ','Laguz','Water','Flow, intuition, the deep, feelings that move you. Go with the current.','Overwhelm, confusion, intuition ignored. Do not swim against the tide.'],
    ['ᛜ','Ingwaz','Fertility','Gestation, inner work completing, potential ready to release. A seed matured.',''],
    ['ᛞ','Dagaz','The Dawn','Breakthrough, a new day, light flooding in, transformation. The turning point.',''],
    ['ᛟ','Othala','Heritage','Home, inheritance, what you truly value, belonging. Your roots and worth.','Rootlessness, clinging to the old, bad inheritance. Choose what to keep.']
  ];

  /* ===================== 5. I CHING — 64 hexagrams ===================== */
  var TRI = { qian: '111', dui: '110', li: '101', zhen: '100', xun: '011', kan: '010', gen: '001', kun: '000' };
  var TRI_NAME = { qian: 'Heaven ☰', dui: 'Lake ☱', li: 'Fire ☲', zhen: 'Thunder ☳', xun: 'Wind ☴', kan: 'Water ☵', gen: 'Mountain ☶', kun: 'Earth ☷' };
  // [number, name, upper, lower, original guidance]  (validated: 64 unique, King Wen pairing holds)
  var HEX = [
    [1,'The Creative','qian','qian','Pure creative force. The time favours bold, honest action in line with your highest aim. Act, but stay upright.'],
    [2,'The Receptive','kun','kun','Yielding, supportive power. Do not lead now — nourish, follow, and let things take form through devotion.'],
    [3,'Difficulty at the Beginning','kan','zhen','A hard, tangled start. Growth is there but chaotic; find helpers and bring order patiently. Do not force.'],
    [4,'Youthful Folly','gen','kan','Inexperience seeking guidance. Ask sincerely and heed the answer once. Teach, or learn, with patience.'],
    [5,'Waiting','kan','qian','Strength that must wait. Danger ahead means do not rush. Nourish yourself, stay sincere; the time will come.'],
    [6,'Conflict','qian','kan','A genuine dispute. Be clear and cautious, seek a fair mediator, and do not push to the bitter end.'],
    [7,'The Army','kun','kan','Disciplined collective effort. Success needs a trusted leader and a just cause. Order over force.'],
    [8,'Holding Together','kan','kun','Union and belonging. Join with the sincere, be the centre others can trust. Come together without delay.'],
    [9,'Small Taming','xun','qian','Gentle restraint of great force. Only small influence is possible now; refine details and wait for the fuller moment.'],
    [10,'Treading','qian','dui','Walking a careful path near power. Conduct yourself with courtesy and firmness; tread lightly and you pass safely.'],
    [11,'Peace','kun','qian','Heaven and earth in harmony. A flourishing, open time. Nurture what is good and keep communication flowing.'],
    [12,'Standstill','qian','kun','Things do not connect; a stagnant, closed time. Withdraw, hold to your principles, and wait it out with integrity.'],
    [13,'Fellowship','qian','li','Open community with shared purpose. Success comes through sincerity in the open, not private cliques.'],
    [14,'Great Possession','li','qian','Abundance clearly held. Great resources and favour — stay modest and generous, and the blessing lasts.'],
    [15,'Modesty','kun','gen','Greatness that stays low. Humility now brings honour and carries things through. Keep your worth quiet.'],
    [16,'Enthusiasm','zhen','kun','Inspired, contagious energy. Align people around a shared mood and move; readiness and timing matter.'],
    [17,'Following','dui','zhen','Adapting and being followed. Lead by serving the moment; be worth following, and follow what is right.'],
    [18,'Work on the Decayed','gen','xun','Repairing what was spoiled. Face the inherited mess honestly; careful work restores it. Do not look away.'],
    [19,'Approach','kun','dui','Something good drawing near. Meet rising opportunity with warmth and care, mindful that no spring lasts forever.'],
    [20,'Contemplation','xun','kun','Standing back to see clearly. Observe, reflect, and let your own example be the quiet teaching.'],
    [21,'Biting Through','li','zhen','A real obstacle must be dealt with. Be decisive and fair; clear the blockage cleanly, like biting through.'],
    [22,'Grace','gen','li','Beauty and good form. Grace adorns, but let substance lead; keep your adornment honest and gentle.'],
    [23,'Splitting Apart','gen','kun','Things falling away. A time of decline — do not act against it. Stay still, protect the foundation, wait.'],
    [24,'Return','kun','zhen','The turning point; light returns. A new cycle begins quietly. Rest, then move with the fresh energy. All comes back.'],
    [25,'Innocence','qian','zhen','Natural, unpremeditated action. Act from a clear and honest heart; drop hidden motives and the way opens.'],
    [26,'Great Taming','gen','qian','Great force held and stored. Restraint builds power; feed your mind, hold back, and great things become possible.'],
    [27,'Nourishment','gen','zhen','What you take in and give out. Mind what you feed your body, mind and words. Nourish rightly.'],
    [28,'Preponderance of the Great','dui','xun','Too much weight on a weak beam. Extraordinary times, under strain. Act, but shore up the structure before it breaks.'],
    [29,'The Abysmal','kan','kan','Repeated danger, deep water. Keep your heart sincere and steady; flow through the ravine without losing yourself.'],
    [30,'The Clinging','li','li','Fire, clarity, dependence on what we cling to. Be radiant but attached to the good. Cultivate clear awareness.'],
    [31,'Influence','dui','gen','Mutual attraction, being moved. Stay open and receptive; genuine influence works gently, not by pressure.'],
    [32,'Duration','zhen','xun','Lasting through time. Endure by renewing within a steady form. Keep going; constancy, not rigidity, wins.'],
    [33,'Retreat','qian','gen','A strategic withdrawal. Step back from what you cannot win now, with dignity and timing. Retreat is strength here.'],
    [34,'Great Power','zhen','qian','Great strength available. Power must be joined to what is right, or it harms. Advance, but do not ram ahead.'],
    [35,'Progress','li','kun','Easy, rising advancement. The way is open and bright; move forward generously and let your light be useful.'],
    [36,'Darkening of the Light','kun','li','Light wounded, hidden. In a dark climate, veil your brilliance and keep your inner light alive. Endure quietly.'],
    [37,'The Family','xun','li','Order within the home. Each in their right place, warmth and clear roles. Tend your closest circle first.'],
    [38,'Opposition','li','dui','Misunderstanding, pulling apart. Differences, not enemies. In small matters, seek the common ground; do not force unity.'],
    [39,'Obstruction','kan','gen','A real obstacle in the path. Stop, turn inward, and seek help and allies. The block asks you to grow, not to shove.'],
    [40,'Deliverance','zhen','kan','Release after tension; the storm breaks. Resolve things, forgive, and return to normal life promptly. Let it go.'],
    [41,'Decrease','gen','dui','Giving something up for later gain. Simplify, spend less, offer sincerely. Loss now, rightly done, becomes gain.'],
    [42,'Increase','xun','zhen','A time to grow and give. Energy flows to your aims; act boldly and be generous while the tide is with you.'],
    [43,'Breakthrough','dui','qian','A decisive resolve. Name the wrong openly and act, but without hatred. Resolute and principled carries the day.'],
    [44,'Coming to Meet','qian','xun','An unexpected encounter, something small returning. Be alert to what you let in; stay centred, do not be swept up.'],
    [45,'Gathering Together','dui','kun','People drawing into one. Rally around a worthy centre and shared feeling. Prepare for what large gatherings stir.'],
    [46,'Pushing Upward','kun','xun','Gradual, effortful ascent. Steady growth upward step by step. Push on with devotion; small efforts accumulate.'],
    [47,'Oppression','dui','kan','Exhaustion, being hemmed in. Means are low and spirits tested. Stay true inwardly; say little, endure, outlast it.'],
    [48,'The Well','kan','xun','A deep, shared source. The source is always there; tend it and draw clean. Renew the structures that feed everyone.'],
    [49,'Revolution','dui','li','Necessary, timely change. When the old no longer serves, change it — but only at the right time and for good reason.'],
    [50,'The Cauldron','li','xun','Transformation and nourishment of the spirit. Refine the raw into something fine; feed what is highest in you.'],
    [51,'The Arousing','zhen','zhen','Shock, thunder, a wake-up. Startling events pass; stay composed, laugh, and keep your inner poise. Then act.'],
    [52,'Keeping Still','gen','gen','Stillness, the mountain. Stop striving; quiet the mind. Act only when the moment is truly ripe. Be present, at rest.'],
    [53,'Development','xun','gen','Gradual, rooted progress. Grow like a tree — slowly, in proper stages. Patience and good form bring lasting advance.'],
    [54,'The Marrying Maiden','zhen','dui','A relationship on uneven footing. Know your place in it and act with tact; do not grasp. Beginnings matter more than passion.'],
    [55,'Abundance','zhen','li','A peak of fullness and clarity. Enjoy the high noon, do good while it shines, and accept that fullness does not last.'],
    [56,'The Wanderer','li','gen','A stranger passing through. Travel light, stay courteous and cautious, keep to the right. Make no permanent claims here.'],
    [57,'The Gentle','xun','xun','Gentle, penetrating influence. Like wind, work persistently and quietly in one direction. Small, steady pressure prevails.'],
    [58,'The Joyous','dui','dui','Open-hearted gladness shared. True joy comes from sincerity and good company. Encourage, speak kindly, enjoy.'],
    [59,'Dispersion','xun','kan','Dissolving what is rigid or divided. Melt hard feelings and barriers; reconnect the scattered around a larger purpose.'],
    [60,'Limitation','kan','dui','Healthy limits and measure. Set wise boundaries; thrift and discipline free you. Do not make the limits bitter.'],
    [61,'Inner Truth','xun','dui','Sincerity that moves others. Truth held at the centre reaches even the distant. Be genuine and trust is returned.'],
    [62,'Small Exceeding','zhen','gen','A time for small, careful steps. Do modest things exceptionally well; stay humble and low. Do not overreach now.'],
    [63,'After Completion','kan','li','Order achieved — and fragile. The goal is reached; now the work is to maintain it. Stay watchful as things can slip.'],
    [64,'Before Completion','li','kan','Almost there, the crossing not yet made. Order is near but not won. Be careful at the final step; place each move well.']
  ];
  function hexLines(h) { return (TRI[h[3]] + TRI[h[2]]).split('').map(function (c) { return +c; }); } // bottom->top, 1=yang
  var HEX_BY_LINES = {}; HEX.forEach(function (h) { HEX_BY_LINES[hexLines(h).join('')] = h; });
  var LINE_POS = ['the bottom line', 'the second line', 'the third line', 'the fourth line', 'the fifth line', 'the top line'];

  /* ===================== 6. NUMEROLOGY ===================== */
  var NUMV = { a:1,b:2,c:3,d:4,e:5,f:6,g:7,h:8,i:9,j:1,k:2,l:3,m:4,n:5,o:6,p:7,q:8,r:9,s:1,t:2,u:3,v:4,w:5,x:6,y:7,z:8 };
  var VOWELS = 'aeiou';
  var NUM_MEAN = {
    1: ['The Leader', 'independence, drive, originality — you are here to stand on your own and begin things.'],
    2: ['The Peacemaker', 'sensitivity, partnership, diplomacy — you thrive in connection and quiet strength.'],
    3: ['The Communicator', 'expression, creativity, joy — you are here to delight, create and uplift.'],
    4: ['The Builder', 'order, discipline, reliability — you make solid things that last.'],
    5: ['The Adventurer', 'freedom, change, the senses — you are here to explore and to not be caged.'],
    6: ['The Nurturer', 'responsibility, love, service — home, beauty and care are your gifts.'],
    7: ['The Seeker', 'depth, analysis, the inner life — you are here to understand what is beneath.'],
    8: ['The Powerhouse', 'ambition, mastery of the material, authority — you learn the right use of power.'],
    9: ['The Humanitarian', 'compassion, wisdom, letting go — you are here to give and to serve the whole.'],
    11: ['The Illuminator (master)', 'intuition, inspiration, spiritual insight — a sensitive channel; ground it to use it.'],
    22: ['The Master Builder (master)', 'big visions made real; you can build things that help many. Great potential, great demand.'],
    33: ['The Master Teacher (master)', 'devoted, healing love in service to others; nurture that comes from an overflowing heart.']
  };
  function reduceNum(n, keepMaster) { while (n > 9 && !(keepMaster && (n === 11 || n === 22 || n === 33))) { n = String(n).split('').reduce(function (a, c) { return a + +c; }, 0); } return n; }
  function lettersSum(str, filter) { var s = 0; str.toLowerCase().split('').forEach(function (c) { if (NUMV[c] && (!filter || filter(c))) s += NUMV[c]; }); return s; }
  function numName(n) { return NUM_MEAN[n] ? NUM_MEAN[n][0] : '—'; }
  function numMean(n) { return NUM_MEAN[n] ? NUM_MEAN[n][1] : ''; }

  /* ===================== 7. BREATH ===================== */
  var BREATH = [
    ['Box breathing', [['Breathe in', 4], ['Hold', 4], ['Breathe out', 4], ['Hold', 4]], 'Steadies the nerves; used by athletes and first responders.'],
    ['Calm (4-7-8)', [['Breathe in', 4], ['Hold', 7], ['Breathe out', 8]], 'A longer out-breath to settle the body before sleep or stress.'],
    ['Moon breath', [['Breathe in', 4], ['Breathe out', 6]], 'Gentle and simple — a soft, slow out-breath to come back to yourself.'],
    ['Coherence (5-5)', [['Breathe in', 5], ['Breathe out', 5]], 'Even breathing near six breaths a minute; balances heart and mind.']
  ];

  /* ===================== rendering ===================== */
  function moonToday() {
    if (!A) return null;
    var d = new Date();
    var mlon = norm(A.EclipticGeoMoon(d).lon), slon = norm(A.SunPosition(d).elon);
    var phase = norm(A.MoonPhase(d));
    var msign = Math.floor(mlon / 30), ssign = Math.floor(slon / 30);
    var phName, phIdx;
    if (phase < 22.5 || phase >= 337.5) { phName = 'New Moon'; phIdx = 0; }
    else if (phase < 67.5) { phName = 'Waxing Crescent'; phIdx = 1; }
    else if (phase < 112.5) { phName = 'First Quarter'; phIdx = 2; }
    else if (phase < 157.5) { phName = 'Waxing Gibbous'; phIdx = 3; }
    else if (phase < 202.5) { phName = 'Full Moon'; phIdx = 4; }
    else if (phase < 247.5) { phName = 'Waning Gibbous'; phIdx = 5; }
    else if (phase < 292.5) { phName = 'Last Quarter'; phIdx = 6; }
    else { phName = 'Waning Crescent'; phIdx = 7; }
    return { d: d, msign: msign, ssign: ssign, phName: phName, phIdx: phIdx };
  }
  var PHASE_THEME = [
    'a clean slate — set an intention and plant the seed',
    'building momentum — take the first small action',
    'a decision point — push through the first resistance',
    'refine and adjust — tend what is growing',
    'fullness and clarity — celebrate, and see what is complete',
    'gratitude and sharing — give some of the harvest away',
    'release and forgive — let go of what did not work',
    'rest and reflect — turn inward before the next cycle'
  ];
  var AFFIRM = {
    Fire: ['I act with courage and warmth.', 'My energy is a gift I give wisely.', 'I lead with an open heart.', 'I begin, and I trust myself.'],
    Earth: ['I am steady, grounded and enough.', 'I build my life one honest step at a time.', 'I give my body what it needs.', 'Slow is also strong.'],
    Air: ['My mind is clear and my words are kind.', 'I am open to new ideas and to change.', 'I connect with ease and with honesty.', 'I can hold two truths at once.'],
    Water: ['I honour my feelings without drowning in them.', 'I give and receive care freely.', 'My intuition is wise; I listen to it.', 'I let what must pass, pass.']
  };
  var JOURNAL = [
    'What is one thing I am ready to begin?',
    'Where in my life do I need more courage — and where more rest?',
    'What am I holding onto that I could gently set down?',
    'Who or what am I grateful for today, and have I told them?',
    'What does my body need from me right now?',
    'What truth have I been avoiding saying out loud?',
    'When did I last feel fully myself, and what was present?',
    'What would the kindest version of me do next?'
  ];
  function todayHTML() {
    var m = moonToday();
    if (!m) return '<p>The sky engine did not load, so today\'s guidance is unavailable. The other tabs still work.</p>';
    var el = ELEM[m.msign % 4];
    var s = seed(m.d.toISOString().slice(0, 10) + el);
    var aff = pick(AFFIRM[el], s);
    var jr = pick(JOURNAL, s >> 3);
    var arch = ARCH[m.msign];
    return '<p class="big3">☾ ' + m.phName + ' in ' + SG[m.msign] + ' ' + SIGNS[m.msign] + '</p>' +
      '<p class="q">Today is ' + PHASE_THEME[m.phIdx] + '.</p>' +
      '<p>The Moon moves through <b>' + SIGNS[m.msign] + '</b> (' + el.toLowerCase() + '), colouring the mood with <i>' + esc(arch[0].toLowerCase().replace('the ', '')) + '</i> energy. The Sun is in ' + SIGNS[m.ssign] + ' season.</p>' +
      '<h3>Today\'s affirmation</h3><p class="q">&ldquo;' + esc(aff) + '&rdquo;</p>' +
      '<h3>Intention</h3><p>Name one small thing that fits ' + esc(PHASE_THEME[m.phIdx].split('—')[0].trim()) + '. Write it where you\'ll see it.</p>' +
      '<h3>A practice</h3><p>' + esc(CHAK[m.phIdx % 7][8]) + '</p>' +
      '<h3>Journal prompt</h3><p class="q">' + esc(jr) + '</p>' +
      '<p class="trad">Moon sign & phase are real astronomy; the guidance is a daily self-help reflection, the same for everyone today.</p>';
  }

  function archHTML() {
    var h = '<h3>Your sky archetypes</h3>';
    var charts = []; try { charts = JSON.parse(localStorage.getItem('sky.charts') || '[]'); } catch (e) {}
    h += '<p>Pick your Sun sign, or read from a saved birth chart for Sun · Moon · Rising.</p>' +
      '<div class="row"><select id="iwSun">' + SIGNS.map(function (s, i) { return '<option value="' + i + '">' + SG[i] + ' ' + s + '</option>'; }).join('') + '</select>';
    if (charts.length && window.SarahReadings && SarahReadings.compute) {
      h += '<select id="iwChart"><option value="">— or a saved chart —</option>' + charts.map(function (c, i) { return '<option value="' + i + '">' + esc(c.name || c.date) + '</option>'; }).join('') + '</select>';
    }
    h += '</div><div id="iwArchOut"></div>';
    h += '<h3 style="margin-top:18px">The twelve inner archetypes</h3><p class="trad">Patterns of the psyche (after C. G. Jung). We each carry all twelve; a few lead.</p>';
    h += '<table class="ct"><tbody>' + JUNG.map(function (j) { return '<tr><td><b>' + esc(j[0]) + '</b></td><td>' + esc(j[1]) + '</td></tr>'; }).join('') + '</tbody></table>';
    return h;
  }
  function archCard(i, label) {
    var a = ARCH[i];
    return '<div class="iwcard"><div class="iwct">' + (label ? '<span class="iwcl">' + esc(label) + '</span> ' : '') + SG[i] + ' ' + a[0] + ' <span class="trad">· ' + a[1] + '</span></div>' +
      '<p>' + esc(a[2]) + '</p><p class="trad">' + esc(a[3]) + '</p><p class="q">&ldquo;' + esc(a[4]) + '&rdquo;</p></div>';
  }
  function signsFromChart(rec) {
    try {
      var d = rec.date.split('-'), t = (rec.time || '12:00').split(':');
      var inp = { y: +d[0], mo: +d[1], d: +d[2], h: +t[0], mi: +t[1], tz: rec.tz, lat: +rec.lat, lon: +rec.lon, houses: rec.houses || 'placidus', sidereal: rec.zod === 'sid' };
      var c = SarahReadings.compute(inp);
      var sun = Math.floor(c.pl[0].slon / 30), moon = Math.floor(c.pl[1].slon / 30), asc = Math.floor(norm(c.an.asc - c.ay) / 30);
      return { sun: sun, moon: moon, asc: asc };
    } catch (e) { return null; }
  }

  function chakHTML() {
    return '<p class="trad">Seven centres of the subtle body (yogic tradition) — a map for where you feel open or stuck.</p>' +
      CHAK.map(function (c) {
        return '<div class="iwcard" style="border-left:5px solid ' + c[2] + '"><div class="iwct">' + esc(c[0]) + ' <span class="trad">· ' + esc(c[1]) + ' · ' + esc(c[5]) + ' · ' + esc(c[3]) + ' · seed “' + esc(c[4]) + '”</span></div>' +
          '<p>' + esc(c[6]) + '</p><p class="trad">' + esc(c[7]) + '</p><p><b>Practice:</b> ' + esc(c[8]) + '</p></div>';
      }).join('');
  }

  function runeDraw(n) {
    var idx = [], pool = RUNE.map(function (_, i) { return i; });
    for (var k = 0; k < n; k++) { var j = rnd(pool.length); idx.push(pool[j]); pool.splice(j, 1); }
    return idx.map(function (i) { return { i: i, rev: RUNE[i][4] ? rnd(2) === 1 : false }; });
  }
  function runeCard(x, pos) {
    var r = RUNE[x.i];
    return '<div class="iwcard"><div class="iwrune">' + r[0] + '</div><div class="iwct">' + (pos ? pos + ': ' : '') + esc(r[1]) + ' <span class="trad">· ' + esc(r[2]) + (x.rev ? ' · reversed' : '') + '</span></div>' +
      '<p>' + esc(x.rev ? r[4] : r[3]) + '</p></div>';
  }
  function runeHTML() {
    return '<p class="trad">Elder Futhark — the oldest runic alphabet. A quiet mirror, not a prediction.</p>' +
      '<div class="row"><button class="go" data-rune="1">Draw one rune</button><button data-rune="3">Three runes (past · present · future)</button></div>' +
      '<div id="iwRuneOut"></div>';
  }

  function tossLines() { // six lines bottom->top; each: 6 or 9 (changing), 7 (young yang), 8 (young yin)
    var ls = [];
    for (var i = 0; i < 6; i++) { var s = (rnd(2) ? 3 : 2) + (rnd(2) ? 3 : 2) + (rnd(2) ? 3 : 2); ls.push(s); }
    return ls;
  }
  function lineYang(v) { return v === 9 || v === 7; } // odd sum = yang
  function hexFromTosses(ls, transformed) {
    return ls.map(function (v) { var yang = lineYang(v); if (transformed) { if (v === 6) yang = true; else if (v === 9) yang = false; } return yang ? 1 : 0; }).join('');
  }
  function drawHexSVG(bits, changing) { // bits bottom->top string; changing = array of bool bottom->top
    var y = 0, rows = '';
    for (var i = 5; i >= 0; i--) { // draw top line first
      var yang = bits[i] === '1', ch = changing && changing[i];
      var col = ch ? '#ff6ec7' : '#cdb8ff';
      if (yang) rows += '<rect x="0" y="' + y + '" width="80" height="8" rx="2" fill="' + col + '"/>';
      else { rows += '<rect x="0" y="' + y + '" width="34" height="8" rx="2" fill="' + col + '"/><rect x="46" y="' + y + '" width="34" height="8" rx="2" fill="' + col + '"/>'; }
      y += 14;
    }
    return '<svg class="iwhex" viewBox="0 0 80 ' + y + '" width="80" height="' + y + '" aria-hidden="true">' + rows + '</svg>';
  }
  function hexReport(bits) { var h = HEX_BY_LINES[bits]; return h || [0, 'Unknown', '', '', '']; }
  function ichingCast() {
    var ls = tossLines();
    var primary = hexFromTosses(ls, false);
    var changing = ls.map(function (v) { return v === 6 || v === 9; });
    var anyChange = changing.some(Boolean);
    var hp = hexReport(primary);
    var h = '<div class="iwhexrow">' + drawHexSVG(primary, changing) +
      '<div><div class="iwct">Hexagram ' + hp[0] + ' · ' + esc(hp[1]) + '</div>' +
      '<p class="trad">' + TRI_NAME[hp[2]] + ' over ' + TRI_NAME[hp[3]] + '</p></div></div>' +
      '<p>' + esc(hp[4]) + '</p>';
    if (anyChange) {
      var moving = [];
      changing.forEach(function (c, i) { if (c) moving.push(LINE_POS[i] + (ls[i] === 9 ? ' (old yang → changing)' : ' (old yin → changing)')); });
      var secondary = hexFromTosses(ls, true), hs = hexReport(secondary);
      h += '<p class="trad"><b>Changing lines:</b> ' + moving.join('; ') + '. These mark where the situation is in motion — pay them special attention.</p>';
      h += '<div class="iwhexrow" style="margin-top:10px">' + drawHexSVG(secondary, null) +
        '<div><div class="iwct">becomes Hexagram ' + hs[0] + ' · ' + esc(hs[1]) + '</div><p class="trad">' + TRI_NAME[hs[2]] + ' over ' + TRI_NAME[hs[3]] + '</p></div></div>' +
        '<p>' + esc(hs[4]) + '</p>';
    } else {
      h += '<p class="trad">No changing lines — the situation is stable for now.</p>';
    }
    return h;
  }
  function ichingHTML() {
    return '<p class="trad">The Book of Changes. Hold a question in mind, then cast — three coins, six times, as tradition has it.</p>' +
      '<div class="row"><input id="iwQ" type="text" placeholder="Your question (optional, stays on this device)"></div>' +
      '<div class="row"><button class="go" id="iwCast">Cast the coins</button></div><div id="iwHexOut"></div>';
  }

  function numHTML() {
    return '<p class="trad">Pythagorean numerology — numbers as a mirror of character. Your full birth name and birth date, both private to this device.</p>' +
      '<div class="row"><input id="iwName" type="text" placeholder="Full birth name (as on the certificate)"></div>' +
      '<label>Birth date <input id="iwDate" type="date"></label>' +
      '<div class="row"><button class="go" id="iwNum">Read my numbers</button></div><div id="iwNumOut"></div>';
  }
  function numReport(name, dateStr) {
    var out = '';
    function row(label, n, note) { return '<tr><td><b>' + label + '</b></td><td style="text-align:center;font-size:18px;color:#ff6ec7">' + n + '</td><td>' + esc(numName(n)) + ' — ' + esc(numMean(n)) + (note ? ' <span class="trad">' + note + '</span>' : '') + '</td></tr>'; }
    out += '<table class="ct"><tbody>';
    if (dateStr) {
      var p = dateStr.split('-'); // yyyy-mm-dd
      var lp = reduceNum(reduceNum(+p[0], false) + reduceNum(+p[1], true) + reduceNum(+p[2], true), true);
      out += row('Life Path', lp, '(who you are here to become)');
      var now = new Date(), py = reduceNum(reduceNum(+p[1], false) + reduceNum(+p[2], false) + reduceNum(now.getFullYear(), false), false);
      out += row('Personal Year (' + now.getFullYear() + ')', py, '(this year\'s theme)');
    }
    if (name && /[a-z]/i.test(name)) {
      var expr = reduceNum(lettersSum(name, null), true);
      var soul = reduceNum(lettersSum(name, function (c) { return VOWELS.indexOf(c) >= 0; }), true);
      var pers = reduceNum(lettersSum(name, function (c) { return VOWELS.indexOf(c) < 0; }), true);
      out += row('Expression', expr, '(your natural gifts)');
      out += row('Soul Urge', soul, '(what your heart wants)');
      out += row('Personality', pers, '(how others first see you)');
    }
    out += '</tbody></table>';
    if (!dateStr && !(name && /[a-z]/i.test(name))) out = '<p>Enter a name, a birth date, or both.</p>';
    return out;
  }

  function breathHTML() {
    return '<p class="trad">A simple breathing guide. Follow the circle; let the numbers set the pace.</p>' +
      '<div class="row"><select id="iwBreath">' + BREATH.map(function (b, i) { return '<option value="' + i + '">' + esc(b[0]) + '</option>'; }).join('') + '</select>' +
      '<select id="iwBreathMin"><option value="1">1 min</option><option value="2">2 min</option><option value="3" selected>3 min</option><option value="5">5 min</option></select>' +
      '<button class="go" id="iwBreathBtn">Begin</button></div>' +
      '<p id="iwBreathNote" class="trad"></p>' +
      '<div id="iwBreathStage"><div id="iwBreathCircle"><span id="iwBreathLabel">Ready</span></div><div id="iwBreathCount"></div></div>';
  }
  var breathTimer = null, breathEnd = 0;
  function stopBreath() { if (breathTimer) { clearTimeout(breathTimer); breathTimer = null; } var b = $('iwBreathBtn'); if (b) b.textContent = 'Begin'; }
  function runBreath() {
    var sel = +$('iwBreath').value, pat = BREATH[sel][1], mins = +$('iwBreathMin').value;
    $('iwBreathNote').textContent = BREATH[sel][2];
    var circle = $('iwBreathCircle'), label = $('iwBreathLabel'), count = $('iwBreathCount');
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    breathEnd = Date.now() + mins * 60000; var step = 0, cycles = 0;
    function phase() {
      if (Date.now() >= breathEnd) { stopBreath(); label.textContent = 'Done — well breathed'; count.textContent = cycles + ' cycles'; circle.className = ''; return; }
      var p = pat[step % pat.length], name = p[0], secs = p[1];
      label.textContent = name;
      circle.className = reduce ? '' : (name.indexOf('in') >= 0 ? 'bin' : name.indexOf('out') >= 0 ? 'bout' : 'bhold');
      if (!reduce) circle.style.transitionDuration = secs + 's';
      var remaining = secs;
      count.textContent = remaining + '';
      var tick = setInterval(function () { remaining--; count.textContent = remaining > 0 ? remaining + '' : ''; }, 1000);
      breathTimer = setTimeout(function () { clearInterval(tick); step++; if (step % pat.length === 0) cycles++; phase(); }, secs * 1000);
    }
    phase();
  }

  /* ===================== sheet ===================== */
  var TABS = [['today', 'Today'], ['arch', 'Archetypes'], ['chakra', 'Chakras'], ['iching', 'I Ching'], ['rune', 'Runes'], ['num', 'Numbers'], ['breath', 'Breathe']];
  function render(tab) {
    var body = $('iwBody'); if (!body) return;
    stopBreath();
    if (tab === 'today') body.innerHTML = todayHTML();
    else if (tab === 'arch') { body.innerHTML = archHTML(); bindArch(); }
    else if (tab === 'chakra') body.innerHTML = chakHTML();
    else if (tab === 'iching') { body.innerHTML = ichingHTML(); $('iwCast').onclick = function () { $('iwHexOut').innerHTML = ichingCast(); }; }
    else if (tab === 'rune') { body.innerHTML = runeHTML(); body.querySelectorAll('[data-rune]').forEach(function (b) { b.onclick = function () { var n = +b.dataset.rune; var dr = runeDraw(n); $('iwRuneOut').innerHTML = n === 1 ? runeCard(dr[0], '') : ['Past', 'Present', 'Future'].map(function (p, i) { return runeCard(dr[i], p); }).join(''); }; }); }
    else if (tab === 'num') { body.innerHTML = numHTML(); $('iwNum').onclick = function () { $('iwNumOut').innerHTML = numReport($('iwName').value.trim(), $('iwDate').value); }; }
    else if (tab === 'breath') { body.innerHTML = breathHTML(); $('iwBreathBtn').onclick = function () { if (breathTimer) { stopBreath(); $('iwBreathLabel').textContent = 'Paused'; } else { this.textContent = 'Stop'; runBreath(); } }; }
    body.scrollTop = 0;
  }
  function bindArch() {
    var out = $('iwArchOut');
    function show() {
      var sel = $('iwChart'), rec = null;
      if (sel && sel.value !== '') { try { rec = JSON.parse(localStorage.getItem('sky.charts') || '[]')[+sel.value]; } catch (e) {} }
      if (rec) {
        var s = signsFromChart(rec);
        if (s) { out.innerHTML = archCard(s.sun, 'Sun') + archCard(s.moon, 'Moon') + archCard(s.asc, 'Rising'); return; }
        out.innerHTML = '<p class="trad">Could not read that chart; showing your chosen Sun sign.</p>' + archCard(+$('iwSun').value, 'Sun');
        return;
      }
      out.innerHTML = archCard(+$('iwSun').value, 'Sun');
    }
    $('iwSun').onchange = function () { var sel = $('iwChart'); if (sel) sel.value = ''; show(); };
    if ($('iwChart')) $('iwChart').onchange = show;
    show();
  }
  function build() {
    var m = document.createElement('div'); m.id = 'inner'; m.hidden = true;
    m.innerHTML = '<div class="rbox"><div class="rhead"><b>🧭 Inner work</b><div class="rtabs" id="iwTabs">' +
      TABS.map(function (t, i) { return '<button data-iw="' + t[0] + '"' + (i === 0 ? ' class="on"' : '') + '>' + t[1] + '</button>'; }).join('') +
      '</div><button id="iwClose" aria-label="Close">×</button></div><div class="rbody" id="iwBody"></div></div>';
    document.body.appendChild(m);
    m.querySelectorAll('#iwTabs button').forEach(function (b) {
      b.onclick = function () { m.querySelectorAll('#iwTabs button').forEach(function (x) { x.classList.toggle('on', x === b); }); render(b.dataset.iw); };
    });
    $('iwClose').onclick = function () { stopBreath(); m.hidden = true; };
    render('today');
  }
  window.SarahInner = {
    open: function (tab) { var m = $('inner'); if (!m) { build(); m = $('inner'); } m.hidden = false; var btn = m.querySelector('[data-iw="' + (tab || 'today') + '"]'); if (btn) btn.click(); },
    isOpen: function () { var m = $('inner'); return m && !m.hidden; },
    close: function () { var m = $('inner'); if (m) { stopBreath(); m.hidden = true; } },
    _data: { HEX: HEX, RUNE: RUNE, CHAK: CHAK, ARCH: ARCH, JUNG: JUNG } // exposed for tests
  };
})();
