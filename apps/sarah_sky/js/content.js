// Text content: surveys, guided tour, lessons and classroom activities. Plain language, ages ~11 and up.
export const SURVEYS = [
  { id: "P/Mellinger/color", label: "Whole sky, as the eye sees it (Mellinger photo mosaic)", band: "visible light" },
  { id: "P/DSS2/color", label: "Digitized Sky Survey (detailed visible light)", band: "visible light" },
  { id: "P/2MASS/color", label: "2MASS infrared (sees through dust)", band: "near infrared" },
  { id: "P/allWISE/color", label: "WISE mid-infrared (warm dust, hidden stars)", band: "mid infrared" },
  { id: "CDS/P/DM/I/355/gaiadr3", label: "Gaia DR3: how many stars per patch of sky", band: "star counts (1.8 billion stars)" },
  { id: "CDS/P/PLANCK/R2/HFI/color", label: "Planck high-frequency microwaves (cold dust; CMB behind it)", band: "microwaves" },
  { id: "P/Fermi/color", label: "Fermi gamma rays (the most energetic light)", band: "gamma rays" },
  { id: "P/VTSS/Ha", label: "Hydrogen-alpha glow (gas lit by hot stars)", band: "H-alpha" },
];

// ra, dec in degrees (J2000); fov in degrees.
export const TOUR = [
  { title: "The whole sky at once", ra: 266.4, dec: -29.0, fov: 360, survey: "P/Mellinger/color",
    text: "This is the entire sky around Earth, unrolled like a map of the world. The bright band is the Milky Way: our own galaxy seen from the inside. Its centre is in the middle of the picture." },
  { title: "Orion, the hunter", ra: 83.8, dec: 0.0, fov: 28, survey: "P/DSS2/color", layers: ["constellations"],
    text: "Constellations are patterns people drew between bright stars. The stars in Orion are not neighbours: Betelgeuse is about 550 light-years away, Rigel about 860." },
  { title: "A star nursery: the Orion Nebula (M42)", ra: 83.82, dec: -5.39, fov: 1.6, survey: "P/DSS2/color",
    text: "A cloud of gas and dust about 1,300 light-years away where new stars are being born right now. You can see it with binoculars just below Orion's belt." },
  { title: "The heart of our galaxy", ra: 266.42, dec: -29.01, fov: 8, survey: "P/2MASS/color",
    text: "In visible light, dust hides the galactic centre. Infrared light passes through dust, so here we see millions of stars, and a black hole four million times the mass of the Sun sits in the middle." },
  { title: "The Pleiades (M45)", ra: 56.75, dec: 24.12, fov: 2.5, survey: "P/DSS2/color",
    text: "A family of young stars born together about 100 million years ago, 440 light-years away. The blue haze is dust reflecting their light." },
  { title: "Another galaxy: Andromeda (M31)", ra: 10.68, dec: 41.27, fov: 4, survey: "P/DSS2/color",
    text: "About 2.5 million light-years away: the light you see left it before humans existed. It holds roughly a trillion stars and is heading towards the Milky Way." },
  { title: "The Large Magellanic Cloud", ra: 80.89, dec: -69.76, fov: 12, survey: "P/DSS2/color",
    text: "A small galaxy orbiting our own, visible to the naked eye from the Southern Hemisphere." },
  { title: "Counting stars: the Gaia map", ra: 266.4, dec: -29.0, fov: 360, survey: "CDS/P/DM/I/355/gaiadr3",
    text: "The European Space Agency's Gaia spacecraft measured the positions, distances and motions of 1.8 billion stars. Brighter means more stars in that patch. The AEGIS Star Mapper re-checked 192 million of them." },
  { title: "The microwave sky", ra: 266.4, dec: -29.0, fov: 360, survey: "CDS/P/PLANCK/R2/HFI/color",
    text: "The Planck satellite mapped microwaves. At these frequencies we mostly see cold dust in our galaxy. Behind it lies the oldest light there is, from 380,000 years after the Big Bang: the cosmic microwave background." },
  { title: "Science that checks itself", ra: 266.4, dec: -29.0, fov: 360, survey: "P/Mellinger/color", layers: ["aegis"],
    text: "The coloured dots (when loaded) are stars the AEGIS survey flagged as unusual. They are candidates, not discoveries: each one needs checking. Open 'AEGIS stars' to help." },
];

export const LESSONS = [
  { title: "How to read this map", body: `<p><b>Right ascension (RA)</b> and <b>declination (Dec)</b> are the sky's longitude and latitude. The <b>field of view</b> is how wide a slice of sky you see: the full Moon is half a degree across.</p><p>Drag to move, scroll or pinch to zoom, and click anything for details.</p>` },
  { title: "Light comes in many colours", body: `<p>Our eyes see only visible light. Telescopes also see infrared (heat), microwaves, X-rays and gamma rays. Switch the <b>Sky picture</b> in Layers and look at the same place in different kinds of light: each shows something the others hide.</p>` },
  { title: "How far away are the stars?", body: `<p>Hold a finger at arm's length and blink one eye, then the other: your finger jumps. Stars do the same as Earth goes round the Sun. That tiny jump is the <b>parallax</b>, and it gives the distance. Gaia measured it for over a billion stars, to the width of a coin seen on the Moon.</p>` },
  { title: "Our galaxy, the Milky Way", body: `<p>The Sun is one of a few hundred billion stars in a flat, spinning disc about 100,000 light-years across. We live inside the disc, so we see it edge-on as a band across the sky.</p>` },
  { title: "The first light and the first instant", body: `<p>The cosmic microwave background is light from when the universe was 380,000 years old. Its tiny ripples were seeded in the first fraction of a second, during <b>inflation</b>, a burst of expansion. Scientists propose models of inflation (AEGIS's is called SERAPIS) and future telescopes will test them by measuring those ripples more precisely. A proposed model is a question, not an answer, until the data decide.</p>` },
  { title: "How scientists avoid fooling themselves", body: `<p>It is easy to see patterns that are not there. One defence is to <b>write down the test and its pass/fail rule before looking at the data</b>, and lock it so it cannot be changed quietly. AEGIS does this for every calculation. When you review flagged stars, decide what would convince you <i>before</i> you look.</p>` },
];

export const ACTIVITIES = [
  { title: "Same sky, different light (15 min)", body: "Pick one place (the galactic centre, Orion). Look at it in visible light, infrared and Gaia star counts. Write one thing each picture shows that the others do not." },
  { title: "Planet hunt (20 min, any evening)", body: "Use the Tonight panel with your town's location. Which planets are up after sunset? Go outside, find one, and sketch where it is compared with the nearest bright star. Check again a week later: has it moved?" },
  { title: "Be the reviewer (25 min)", body: "In AEGIS stars, open five flagged stars. Before you vote, agree as a group what would make a flag 'look real' (for example, a high speed that is far bigger than its error). Then vote, and export the class's reviews." },
];
