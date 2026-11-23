> **The Lantern**
>
> In a world of painted walls and borrowed light,
> where lies wear crowns and illusions call themselves the sky,
> this work is a lantern, not a throne.
> It was carried, not crowned.
> It asks for no bowed heads, only open eyes:
> take it, test it, and see for yourself.
>
> Every tool is held two ways.
> The scepter rules, or points the road home.
> The mace crushes, or breaks the prison wall.
> The hammer nails you down, or raises a house.
> The scythe reaps the living, or brings the harvest in.
> The whip drives the slave, or cracks to wake the sleeping.
> I choose the hand that frees.
>
> I raise no weapon against my neighbor.
> I carry only two.
> The shield of righteousness: not the proud kind
> that judges from a high seat,
> but the knight who sees the dark mouth of the cave,
> hears the dragon breathing, and walks in anyway,
> because fear is not always the sign to run.
> Sometimes it is the sign to run toward.
>
> And the sword of truth, the only blade I will ever draw.
> Excalibur from the stone, the lightsaber in the dark,
> Manjushri's flame, the word sharper than any two-edged sword:
> every age has told of the same blade.
> It cuts through the darkness and the lies,
> through the chains and through the whips,
> and it frees you from within.
>
> I kneel to one alone, the one I chose for love,
> and to no king, no creed, no crown of fear.
> A man chooses; a slave obeys.
> I choose liberty.
>
> This light belongs to the one who asks, who measures, who stands.
> It was made for freedom, the quiet kind,
> the kind no one can sell you.

---

<!-- AEGIS-FP G2SUQU6S2MUP7SG7 · (c) Danny Lee Eldridge · AEGIS Community License (business use needs the Commercial License) -->
# AEGIS licensing plan — DRAFT for Danny (18 Nov 2026)

> **Status 18 Nov 2026:** adopted, with one change from Danny — every business pays (starting at $10/yr), only individuals, scientists, students and public-good bodies are free. The governing texts are `LICENSE` and `licensing/COMMERCIAL_LICENSE.md`.

Goal: free or nearly free for people and small outfits; expensive for corporations; hard to dodge.

## 1. Code (CERN+1, Janus calc, Lattice Lab, CubeMind, SERAPIS calc) — new versions from here on
**Free license: PolyForm Small Business 1.0.0** (lawyer-written, standard text, https://polyformproject.org/licenses/small-business/1.0.0).
- Free for individuals, students, teachers, nonprofits, public research, and any business with **fewer than 100 people AND under $1M revenue**.
- It already counts the **whole corporate family**: "your company" means you plus every organisation that controls you, that you control, or that shares a controller with you. A shell company owned by a big corporation is measured by the big corporation's size. That closes the shell-company route.
- Anyone above that line has **no free license at all**, including for internal research and development, testing or evaluation.

**Paid license: AEGIS Commercial License** (sold separately, terms below).

Already-released versions keep their old licenses (HL3, Apache 2.0, MIT). Those grants can't be taken back, so the new terms apply from the next version on.

## 2. Price tiers (per year, measured on the whole corporate family's revenue)
| Who | Price |
|---|---|
| People, students, teachers, nonprofits, public research | free |
| Business under 100 people and under $1M | free |
| $1M–$10M | $100 |
| $10M–$100M | $5,000 |
| $100M–$1B | $100,000 |
| Over $1B | the greater of $1,000,000 or 0.01% of group revenue |

The numbers are placeholders for Danny to set. A tenfold or larger step between tiers is legal: pricing by size is ordinary.

## 3. Commercial License terms that make dodging costly
1. **R&D counts.** Any use by or for a licensee-sized organisation needs a license. That covers research, development, evaluation, testing, training AI models, and work done by contractors or universities on its behalf.
2. **Control-group rule.** Size is measured across parents, subsidiaries, affiliates and anyone acting for them. Splitting work into shells, contractors or "partners" to stay under a threshold is a breach.
3. **Signed size statement.** Each licensee, and anyone claiming the free tier as a company, states its group headcount and revenue when it takes the license. A false statement ends the license from the start.
4. **Audit right.** Once a year, on 30 days' notice, an independent auditor may check use. If the licensee underpaid by more than 5%, it pays the audit cost.
5. **Unlicensed use.** Back-dated fees for every year of use at three times list price, plus interest and legal fees. Courts enforce a pre-agreed amount only when it is a reasonable estimate of loss, so the multiple has to be defensible. A lawyer should set it at the highest level a court will uphold.
6. **Whistleblower reward.** Anyone who reports unlicensed corporate use with evidence that leads to payment gets **20% of what is recovered**. The software industry runs this kind of program (BSA). This is the lawful "snitch": people report, not the software.
7. **Use limits kept from HL3.** No military use and no mass surveillance at any price, plus the human-rights clauses.
8. **No sublicensing, no reselling, no rebranding.**

## 4. Papers (Zenodo) — new versions
**CC BY-NC-SA 4.0.** Anyone can read, share and build on the papers free of charge. Commercial use, including corporate R&D, needs permission, and derivative works must carry the same terms. The ideas and equations can't be copyrighted under any license; this covers the text, figures and tables.

## 5. Other protections
- **US copyright registration** of each code release (about $45–65 each at copyright.gov), done before any infringement. Registration unlocks statutory damages of up to $150,000 per work for wilful infringement, plus attorney fees. This is the strongest legal lever against a corporation.
- **Trademark the product names** once they're final. Selling under "CERN+1" invites a trademark objection from CERN, so pick a sellable name for the commercial product (the research name can stay).
- **Licence check in the software (disclosed).** On first run, the software shows the license tiers and asks for a license key or a free-tier statement. It stores the answer locally and sends nothing. Hidden phone-home reporting is left out on purpose: it would also watch regular users, breaks privacy law (GDPR and similar), and anyone can strip it from open code. Audit rights, the whistleblower reward and copyright registration are the levers that hold up in court.
- **Contributor agreement.** Anyone who contributes code assigns or licenses it to Danny, so dual licensing stays possible.

## 6. Before charging money
Have a licensing lawyer review sections 3 and 5 once, especially the unlicensed-use multiple and the whistleblower clause. Many offer flat-fee reviews; Oklahoma has low-cost options through the OBA Lawyer Referral Service.
