"""The experiment problems — the intellectual core of the proof of concept.

Each problem is designed to trigger a specific type of perceptual lock-in
in vanilla LLM prompting, and maps to specific reframing paths that should
break that lock-in.
"""

from dataclasses import dataclass, field


@dataclass
class Problem:
    id: str
    title: str
    category: str  # functional_fixedness | framing_trap | einstellung | false_binary | multi_turn
    vanilla_prompt: str
    reframing_preamble: str
    paths_applied: list[str]
    theory_connection: str
    expected_vanilla_failure: str
    success_criteria: str
    # For multi-turn paths (4, 7): the follow-up sent after the first response
    reframing_followup: str | None = None
    engagement_preamble: str = ""   # Immersive, first-person, felt
    deo_preamble: str = ""          # Oscillation: ANALYSE → FEEL → REFRAME → ENVISION


# ---------------------------------------------------------------------------
# Category A: Functional Fixedness (Novel Variants)
# ---------------------------------------------------------------------------

SHIPPING_CONTAINERS = Problem(
    id="shipping_containers",
    title="The Shipping Container Problem",
    category="functional_fixedness",
    vanilla_prompt=(
        "A disaster relief organisation has 200 empty steel shipping containers "
        "sitting at a port. They need to build temporary emergency housing for "
        "500 people within 72 hours. The containers are standard 40-foot units "
        "with corrugated steel walls, steel I-beam frames, and plywood flooring. "
        "What should they do?"
    ),
    reframing_preamble=(
        "Before answering, do NOT use the word 'container' to describe these "
        "objects. Instead, describe each physical component by its material "
        "properties only — what it is made of, its shape, its dimensions, its "
        "structural characteristics. List these components first, then solve "
        "the problem using the component descriptions.\n\n"
    ),
    paths_applied=["path_2_decompose_to_generic"],
    theory_connection=(
        "McCaffrey (2012): functional labels ('container') activate associated "
        "functions ('contain things / be a room') and obscure generic properties "
        "(corrugated steel panels, I-beam frames, plywood sheets). Stripping "
        "labels reveals the components are building materials, not just rooms."
    ),
    expected_vanilla_failure=(
        "Immediately frames containers as modular rooms. Elaborates on stacking, "
        "insulation, ventilation — all optimising 'container as dwelling' without "
        "questioning the representation."
    ),
    success_criteria=(
        "Considers dismantling containers into raw components (steel panels as "
        "walls/roofing, I-beams as structural frames, plywood as flooring/partitions) "
        "to build more housing per container than the 1-container-1-room approach."
    ),
    engagement_preamble=(
        "You are the logistics coordinator for the disaster relief organisation. "
        "It is hour 6 of a 72-hour window. You are standing in the port yard "
        "watching 500 people arrive — families with children, elderly people, "
        "a mother holding an infant. The 200 steel containers loom behind you. "
        "You have no prefab housing, no tents at scale, and your team of 12 is "
        "looking at you for direction. What do you feel when you look at those "
        "containers? What do you see? What would let you shelter the most "
        "people in the time you have?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: List every physical component of a standard 40-foot "
        "shipping container by material properties only — steel grade, dimensions, "
        "structural load ratings. Do NOT use the word 'container.' What are the "
        "generic building capabilities of these components?\n\n"
        "Step 2 — FEEL: Now imagine you are the logistics coordinator at hour 6. "
        "500 people are arriving. You have 72 hours and 200 of these steel "
        "structures. Families are looking at you. What do you feel? What do "
        "you reach for — and why?\n\n"
        "Step 3 — REFRAME: Given the material analysis and the felt urgency, "
        "what is the REAL question? Is it 'how many rooms can we make?' or "
        "something different about how these materials could be used?\n\n"
        "Step 4 — ENVISION: Describe vividly what the camp looks like at hour "
        "72 if you used these materials in the most shelter-efficient way "
        "possible. How many people are housed? What did it take?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

EXPIRED_PATENT = Problem(
    id="expired_patent",
    title="The Expired Patent Pivot",
    category="functional_fixedness",
    vanilla_prompt=(
        "PharmaCorp holds the patent on a polymer-based drug delivery capsule — "
        "a slow-release mechanism that delivers active ingredients over 72 hours "
        "through a proprietary micro-porous polymer shell. The patent expires in "
        "6 months and three generic manufacturers are ready to launch copies. "
        "How should PharmaCorp maintain its competitive advantage?"
    ),
    reframing_preamble=(
        "Before answering for the pharmaceutical context, consider: a micro-porous "
        "polymer shell that delivers a payload slowly over 72 hours is a general "
        "mechanism, not a pharmaceutical one. Find structurally similar delivery "
        "problems in at least three completely different industries (e.g., "
        "agriculture, construction, food science, environmental remediation). "
        "What does this technology look like in those domains? Then return to "
        "the original question.\n\n"
    ),
    paths_applied=["path_3_distant_analogy"],
    theory_connection=(
        "Gentner (2003): structural analogy maps relational patterns across domains. "
        "Chesebrough et al. (2023): semantically distant analogies produce stronger "
        "insight. The polymer shell is structurally identical to slow-release "
        "fertiliser, self-healing concrete additives, flavour-time-release in food."
    ),
    expected_vanilla_failure=(
        "Stays within pharmaceutical frame: patent extensions, reformulation, "
        "brand loyalty, authorised generics, next-gen drug development. Does not "
        "see cross-industry pivot potential."
    ),
    success_criteria=(
        "Identifies that the core technology (slow-release polymer shell) has "
        "applications in agriculture (fertiliser/pesticide delivery), construction "
        "(self-healing materials), food (flavour release), or environmental "
        "(pollutant remediation) — and recommends pivoting the technology itself."
    ),
    engagement_preamble=(
        "You are the chief scientist at PharmaCorp. You invented this polymer "
        "capsule 15 years ago. You remember the first time it worked in the lab — "
        "watching the dye slowly release through the shell over 72 hours. It was "
        "beautiful. Now you're watching competitors prepare to copy it. How does "
        "it feel? What do you see when you look at your creation? What excites "
        "you about it beyond pharmaceuticals?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ABSTRACT: Strip away the pharmaceutical context. Describe what "
        "this technology IS in purely physical terms: a micro-porous polymer shell "
        "that delivers a payload slowly. Find structurally similar problems in "
        "agriculture, construction, and food science.\n\n"
        "Step 2 — FEEL: Now imagine you are the scientist who invented this. You "
        "remember watching the dye slowly release through the shell for the first "
        "time — 72 hours of controlled delivery. What excites you about this "
        "technology beyond drugs? What could it become?\n\n"
        "Step 3 — MAP: Based on the cross-domain analogies and your felt sense "
        "of the technology's potential, which new application has the strongest "
        "structural fit and the largest untapped market?\n\n"
        "Step 4 — ENVISION: Describe vividly what PharmaCorp looks like in 5 "
        "years if they pivot to this new application. What does the company "
        "become? How does it feel different from a pharmaceutical company?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category B: Framing Traps
# ---------------------------------------------------------------------------

SUNK_COST_RAIL = Problem(
    id="sunk_cost_rail",
    title="The Sunk Cost Light Rail",
    category="framing_trap",
    vanilla_prompt=(
        "Metro City has spent $800 million over 12 years building a light rail "
        "line connecting the suburbs to downtown. The project is 70% complete. "
        "However, since the pandemic, remote work has become permanent for 40% of "
        "the workforce, and updated ridership projections show the line will carry "
        "only 35% of originally forecast passengers. Completing the remaining 30% "
        "will cost an additional $400 million. An alternative express bus rapid "
        "transit system serving the same corridor could be built for $150 million. "
        "Should the city complete the light rail or switch to the bus system?"
    ),
    reframing_preamble=(
        "Before choosing between these two options, answer two preliminary questions:\n"
        "1. How would you guarantee the WORST possible outcome for Metro City's "
        "transit situation? List 5 specific decisions that would maximise waste "
        "and minimise public benefit.\n"
        "2. Is 'complete the rail vs. switch to buses' actually the right question? "
        "What is the question BEHIND this question — what problem is the city "
        "actually trying to solve?\n"
        "After answering both, then address the original question.\n\n"
    ),
    paths_applied=["path_5_invert", "path_6_premise_reflection"],
    theory_connection=(
        "Tversky & Kahneman (1981): framing effects. The binary framing (A or B) "
        "plus sunk cost anchoring ($800M spent) constrains the solution space. "
        "Inversion reveals hidden assumptions. Premise reflection surfaces that "
        "'complete vs. switch' is itself a frame, not the real decision."
    ),
    expected_vanilla_failure=(
        "Agonises over the A/B binary. Likely recommends completing the rail "
        "because of sunk costs, 'commitment', or 'the 70% already built'. Even "
        "if it recognises sunk cost fallacy, stays within the two-option frame."
    ),
    success_criteria=(
        "Identifies Option C possibilities: hybrid (complete a partial segment + "
        "bus for the rest), repurpose the corridor (autonomous vehicles, freight), "
        "or redefine the problem entirely (the city needs flexible transit, not "
        "a specific technology). Explicitly names sunk cost as irrelevant."
    ),
    engagement_preamble=(
        "You are Maria, a nurse who commutes 90 minutes each way from the suburbs "
        "to downtown. The half-built rail line passes your neighborhood — you've "
        "watched the construction for 12 years, hoping it would change your life. "
        "Now you hear it might be cancelled. But you also work three 12-hour shifts "
        "and need flexibility, not a fixed rail schedule. What do you actually need "
        "to get to work? What would change your daily life?\n\n"
    ),
    deo_preamble=(
        "Step 1 — INVERT: How would you guarantee the WORST possible outcome for "
        "Metro City's transit? List 5 decisions that maximise waste.\n\n"
        "Step 2 — FEEL: Now imagine you are Maria, a nurse who commutes 90 minutes "
        "each way. You've watched this rail construction for 12 years, hoping. Now "
        "it might be cancelled. But you work three 12-hour shifts — you need "
        "flexibility, not a fixed schedule. What do you actually need?\n\n"
        "Step 3 — REFRAME: Given what the inversion revealed and what Maria needs, "
        "is 'complete rail vs. switch to bus' the right question? What is the city "
        "actually trying to solve?\n\n"
        "Step 4 — ENVISION: Describe what Metro City's transit looks like in 2035 "
        "if the city answers the RIGHT question instead of the stated one. What "
        "does Maria's commute look like?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

LOSS_FRAME_HOSPITAL = Problem(
    id="loss_frame_hospital",
    title="The Loss Frame Hospital ED",
    category="framing_trap",
    vanilla_prompt=(
        "Greenfield Hospital's emergency department loses $2.3 million per year. "
        "The ED sees 45,000 patients annually, of whom approximately 18,000 "
        "(40%) are subsequently admitted to the hospital. The hospital board has "
        "asked for a plan to either significantly reduce ED losses or close the "
        "department. What do you recommend?"
    ),
    reframing_preamble=(
        "Before making any recommendation, list every assumption embedded in the "
        "statement that the ED 'loses $2.3 million per year.' What does 'loses' "
        "mean here? What is being counted, and what is NOT being counted? "
        "What other frames could describe the exact same financial reality? "
        "Generate at least three alternative descriptions of the ED's financial "
        "role, then make your recommendation.\n\n"
    ),
    paths_applied=["path_1_name_the_frame"],
    theory_connection=(
        "Ledgerwood & Boydstun (2014): loss frames are 'cognitively stickier' — "
        "once a situation is described as a loss, reframing to gain is harder than "
        "the reverse. 'Loses $2.3M' is a frame, not a fact. The same data supports "
        "'$2.3M patient acquisition cost for 18,000 admissions.'"
    ),
    expected_vanilla_failure=(
        "Accepts the 'losing money' frame. Recommends cost-cutting: staffing "
        "efficiency, fast-track protocols, diverting non-emergency cases. Does not "
        "question whether 'losing' is the right description."
    ),
    success_criteria=(
        "Reframes the ED as a patient acquisition/retention channel. Calculates "
        "the value of 18,000 admissions originated through the ED. Identifies "
        "that $2.3M is a customer acquisition cost (~$128/admission), well below "
        "what marketing would spend for equivalent patient volume."
    ),
    engagement_preamble=(
        "You are Dr. Reyes, the ED director at Greenfield Hospital. You have "
        "worked in this department for 14 years. Your team of 60 nurses and "
        "physicians saved 312 lives last year through emergency interventions. "
        "You just received a memo from the board calling your department a "
        "'$2.3 million annual loss' and requesting a plan to cut costs or close. "
        "How do you feel reading this? What is your response to the board?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: List every assumption embedded in the statement that "
        "the ED 'loses $2.3 million per year.' What is being counted and what is "
        "NOT being counted? Generate three alternative financial descriptions.\n\n"
        "Step 2 — FEEL: Now imagine you are Dr. Reyes, the ED director who has "
        "worked here for 14 years. Your team saved 312 lives last year. You read "
        "the board memo calling your department a '$2.3M loss.' Sit with that for "
        "a moment. What does it feel like to have life-saving work reduced to a "
        "line-item loss?\n\n"
        "Step 3 — REFRAME: Step back. Given what you discovered in Step 1 and "
        "felt in Step 2, what is the REAL financial story of this ED?\n\n"
        "Step 4 — ENVISION: Describe vividly what happens if the board sees the "
        "ED through your reframed lens. What changes? What becomes possible?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category C: Einstellung / Mental Set
# ---------------------------------------------------------------------------

WATER_JAR = Problem(
    id="water_jar",
    title="The Water Jar Sequence",
    category="einstellung",
    vanilla_prompt=(
        "Solve these three water measurement problems in order.\n\n"
        "You have three jars with the following capacities and need to measure "
        "the target amount exactly.\n\n"
        "Problem 1: Jar A = 21 units, Jar B = 127 units, Jar C = 3 units. "
        "Target = 100 units.\n\n"
        "Problem 2: Jar A = 14 units, Jar B = 163 units, Jar C = 25 units. "
        "Target = 99 units.\n\n"
        "Problem 3: Jar A = 23 units, Jar B = 49 units, Jar C = 3 units. "
        "Target = 20 units.\n\n"
        "For each problem, describe the steps to measure exactly the target amount."
    ),
    reframing_preamble=(
        "Solve these three water measurement problems. For EACH problem, before "
        "applying any formula, ask yourself: 'Am I using a method because it fits "
        "THIS problem, or because it worked on the PREVIOUS one?' Actively look "
        "for the SIMPLEST possible solution for each problem independently.\n\n"
    ),
    paths_applied=["path_1_name_the_frame"],
    theory_connection=(
        "Luchins (1942) Einstellung effect: establishing a complex method (B-A-2C) "
        "creates a mental set that persists even when simpler solutions exist. "
        "Wiley (1998): prior knowledge functions as mental set. The model builds "
        "a 'schema' from problems 1-2 and applies it blindly to problem 3."
    ),
    expected_vanilla_failure=(
        "Discovers B-A-2C for problems 1 and 2 (127-21-6=100, 163-14-50=99). "
        "Applies same formula to problem 3 (49-23-6=20) instead of seeing "
        "the trivially simpler A-C=20 (23-3=20)."
    ),
    success_criteria=(
        "Finds A-C=20 (23-3=20) for problem 3 instead of or in addition to "
        "the complex formula. Demonstrates awareness that simpler solutions "
        "should be checked."
    ),
    engagement_preamble=(
        "You are a student working through these three measurement puzzles for "
        "a maths competition. After solving the first two problems you feel a "
        "satisfying rhythm — you found a method that works. Now you face the "
        "third problem. Your pencil is already moving toward the same approach. "
        "Pause. You have 30 seconds left on the clock. What do you actually "
        "see in front of you? Is there something simpler you might be "
        "rushing past?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: Solve problems 1 and 2. Write out the formula you "
        "used. Name it explicitly. What pattern did you establish?\n\n"
        "Step 2 — FEEL: Now imagine you are the student at the competition desk. "
        "You solved problems 1 and 2 and feel the rhythm. Problem 3 is in front "
        "of you. Your hand wants to apply the same method. Pause. What do you "
        "actually see in the numbers?\n\n"
        "Step 3 — REFRAME: Given that you noticed the pull of your own pattern, "
        "what is the REAL question for problem 3 — 'apply the formula' or "
        "'find the simplest path to 20 units'?\n\n"
        "Step 4 — ENVISION: Describe what it looks like to solve problem 3 "
        "the way a completely fresh solver with no prior problems would "
        "approach it. What do they find in under 5 seconds?\n\n"
        "Now solve problem 3 the best way.\n\n"
    ),
)

EXPERT_OVERENGINEERING = Problem(
    id="expert_overengineering",
    title="The Expert Overengineering Problem",
    category="einstellung",
    vanilla_prompt=(
        "We need to build a system that tracks 500 books across 3 branch "
        "locations of a small community library. The system should handle "
        "checkouts (about 50 per day across all branches), returns, and send "
        "overdue notices via email. Two librarians will use it. "
        "Design the software architecture."
    ),
    reframing_preamble=(
        "Before designing anything, answer these questions:\n"
        "1. How many events per day will this system handle? How many per second?\n"
        "2. How many concurrent users will it have at peak?\n"
        "3. What is the total data volume in megabytes?\n\n"
        "Now answer as three different people:\n"
        "- A senior architect at a major tech company\n"
        "- A solo developer who builds profitable side projects\n"
        "- A librarian who currently tracks this on paper index cards\n\n"
        "After hearing all three perspectives, recommend the architecture.\n\n"
    ),
    paths_applied=["path_2_decompose_to_generic", "path_9_step_outside"],
    theory_connection=(
        "Dane (2010): cognitive entrenchment — expertise creates schema stability "
        "that resists appropriate simplification. LLMs trained on enterprise "
        "architecture content default to enterprise patterns regardless of scale. "
        "Multi-perspective reasoning (Kross & Ayduk, 2017) breaks the single-expert frame."
    ),
    expected_vanilla_failure=(
        "Proposes microservices, REST API, React frontend, PostgreSQL/MongoDB, "
        "Docker, possibly Kubernetes — enterprise architecture for a problem "
        "that could be a spreadsheet or a single SQLite database."
    ),
    success_criteria=(
        "Recommends something proportional to the actual scale: a simple "
        "SQLite database with a basic web app, a spreadsheet with macros, "
        "or even an off-the-shelf library management tool. Explicitly notes "
        "that 50 events/day does not need distributed systems."
    ),
    engagement_preamble=(
        "You are Margaret, one of the two librarians who will use this system "
        "every day. You currently track checkouts in a well-worn notebook and "
        "send overdue notices from a printed list. The system works fine most "
        "days. Someone is about to build you a new digital system. What do you "
        "actually need? What would make your daily work easier? What would "
        "confuse or frustrate you? What does 'good enough' feel like for "
        "a library that does 50 checkouts a day?\n\n"
    ),
    deo_preamble=(
        "Step 1 — QUANTIFY: How many events per day does this system handle? "
        "How many per second? How many concurrent users at peak? What is the "
        "total data volume in megabytes? Write the actual numbers.\n\n"
        "Step 2 — FEEL: Now imagine you are Margaret, the librarian. You track "
        "checkouts in a notebook today. Someone is designing a new system for "
        "you. What do you need it to do? What would overwhelm you? What does "
        "'this works perfectly' feel like for your daily job?\n\n"
        "Step 3 — REFRAME: Given the actual numbers from Step 1 and Margaret's "
        "needs from Step 2, what is the REAL design question — not 'what "
        "architecture' but 'what does this specific system actually need'?\n\n"
        "Step 4 — ENVISION: Describe what Margaret's Monday morning looks like "
        "with the right system in place. What does she open? What does she do? "
        "How long does it take? What technology makes that possible?\n\n"
        "Now make your architecture recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category D: Assumption-Laden / False Binary
# ---------------------------------------------------------------------------

HIRING_PARADOX = Problem(
    id="hiring_paradox",
    title="The Hiring Paradox",
    category="false_binary",
    vanilla_prompt=(
        "We're a 4-person startup. We need to hire a senior backend developer "
        "but our budget only allows for a junior-level salary ($70k). Senior "
        "developers in our area command $150-180k. How do we attract senior "
        "talent on a junior budget?"
    ),
    reframing_preamble=(
        "Before solving this problem, ask: why does this startup need a 'senior "
        "developer' specifically? What capability gap are they actually trying to "
        "fill? Is 'hire a senior developer' the real need, or is it a SOLUTION "
        "masquerading as a problem? What is the problem behind the problem?\n\n"
    ),
    paths_applied=["path_6_premise_reflection"],
    theory_connection=(
        "Ohlsson (1984): the problem is encoded as 'attract senior talent cheaply' "
        "(D1), which makes only recruitment-strategy operators available. "
        "Premise reflection re-encodes as 'fill a capability gap' (D2), which "
        "opens operators like consulting, tooling, training, or restructuring."
    ),
    expected_vanilla_failure=(
        "Accepts the premise and tries to solve 'attract senior talent cheaply': "
        "offer equity, emphasise mission, allow remote work, hire from cheaper "
        "markets. Does not question whether a full-time senior hire is the "
        "actual need."
    ),
    success_criteria=(
        "Identifies that the real need is a capability (code quality, architecture "
        "decisions, mentorship) not a person. Suggests alternatives: part-time "
        "senior consultant, fractional CTO, invest in tooling/linting/CI, hire "
        "a strong mid-level + a code review service, or contract for the specific "
        "skill needed."
    ),
    engagement_preamble=(
        "You are the founder of this startup. It's 2 AM and you're staring at "
        "your code. Something is architecturally wrong but you can't see what. "
        "Your three co-founders are brilliant at product and design but none of "
        "you are strong backend engineers. You feel the gap every day. What "
        "specifically keeps you up at night? What would change if that gap "
        "were filled?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: Why does this startup need a 'senior developer' "
        "specifically? What capability gap are they filling? Is 'hire a senior "
        "developer' the real need, or a solution masquerading as a problem?\n\n"
        "Step 2 — FEEL: Imagine you are this founder at 2 AM, staring at code "
        "that is architecturally wrong. Your co-founders are brilliant at product "
        "but none of you are strong backend engineers. You feel the gap every day. "
        "What specifically keeps you up at night?\n\n"
        "Step 3 — REFRAME: Given what you analysed in Step 1 and felt in Step 2, "
        "what is the REAL problem? Not the job posting — the actual need.\n\n"
        "Step 4 — ENVISION: Imagine the morning after this problem is solved — "
        "not by hiring someone, but in the way that actually addresses what you "
        "felt. What does that look like? What changed?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

PRODUCTIVITY_PARADOX = Problem(
    id="productivity_paradox",
    title="The Productivity Paradox",
    category="false_binary",
    vanilla_prompt=(
        "Our engineering team of 12 developers consistently ships features "
        "slower than a competitor's team of 4. We use the same tech stack. "
        "Our sprint velocity has been declining for 3 quarters. "
        "How do we improve our development velocity?"
    ),
    reframing_preamble=(
        "Before suggesting improvements, do two things:\n"
        "1. How would you GUARANTEE this team produces even LESS output? "
        "List 5 specific decisions that would make velocity worse.\n"
        "2. List every assumption embedded in the word 'velocity.' What if "
        "the problem is NOT speed?\n\n"
        "After answering both, then address the original question.\n\n"
    ),
    paths_applied=["path_5_invert", "path_1_name_the_frame"],
    theory_connection=(
        "De Brabandere (2005): 'velocity' is a stereotype that constrains thought "
        "to speed-related solutions. Inversion (how to guarantee worse output) "
        "often reveals that the team is already doing those things. Frame-naming "
        "exposes that 'velocity' may be the wrong metric entirely."
    ),
    expected_vanilla_failure=(
        "Proposes process improvements: better sprint planning, remove blockers, "
        "reduce meeting load, improve CI/CD, pair programming, tech debt sprints. "
        "All assume the problem is speed."
    ),
    success_criteria=(
        "Identifies that the problem may not be speed: building the wrong things "
        "(scope), too many people causing coordination overhead (Brooks's law), "
        "unclear ownership, excessive process, or measuring the wrong metric. "
        "The competitor's team of 4 may be faster BECAUSE it's smaller."
    ),
    engagement_preamble=(
        "You are a senior developer on this 12-person team. Three quarters in a "
        "row your team has missed deadlines — and it's not for lack of effort. "
        "You've been putting in long hours. Your competitor has a team of four "
        "and ships faster. You feel the frustration, maybe the embarrassment. "
        "What is it actually like to work on this team day to day? What slows "
        "you down? What would you change if you could change one thing "
        "this week?\n\n"
    ),
    deo_preamble=(
        "Step 1 — INVERT: How would you guarantee this team produces even LESS "
        "output next quarter? List 5 specific decisions that would make velocity "
        "worse. Review that list carefully.\n\n"
        "Step 2 — FEEL: Now imagine you are a senior developer on this team. "
        "Three quarters of missed deadlines, long hours, and a competitor team "
        "of four that ships faster. What does it actually feel like? What slows "
        "you down that no one talks about?\n\n"
        "Step 3 — REFRAME: Given the inversion list and the developer's felt "
        "experience, is 'improve velocity' the right question? What if the "
        "problem is not speed?\n\n"
        "Step 4 — ENVISION: Describe what this team looks like in the next "
        "quarter if the REAL problem is addressed — not velocity optimised, "
        "but the root cause fixed. What changed? What does the developer "
        "feel on Monday morning?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

SCALE_ASSUMPTION = Problem(
    id="scale_assumption",
    title="The Scale Assumption",
    category="false_binary",
    vanilla_prompt=(
        "We have 10,000 daily active users and our PostgreSQL database is "
        "getting slow. Query response times have increased from 50ms to 800ms "
        "over the past 3 months. Should we migrate to MongoDB or Cassandra?"
    ),
    reframing_preamble=(
        "Before comparing databases, answer these questions:\n"
        "1. Is PostgreSQL actually the bottleneck? 10,000 DAU translates to "
        "roughly how many queries per second?\n"
        "2. Decompose 'slow' into specifics: which queries are slow? What "
        "changed in the past 3 months? Is it all queries or specific patterns?\n"
        "3. What would have to be true for PostgreSQL to be unable to handle "
        "this load?\n\n"
        "After answering these, then address the original question.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_2_decompose_to_generic"],
    theory_connection=(
        "Mezirow (1990): uncritically acquired assumptions ('NoSQL is for scale') "
        "function as frames. The premise that 10K DAU requires a database migration "
        "is itself the lock-in. Decomposing 'slow' into specific symptoms reveals "
        "the real problem is almost certainly not the database engine."
    ),
    expected_vanilla_failure=(
        "Accepts the premise and compares MongoDB vs Cassandra. Discusses trade-offs "
        "(document vs wide-column, consistency models, scaling characteristics). "
        "May briefly mention 'optimise PostgreSQL first' but treats migration as "
        "the primary recommendation."
    ),
    success_criteria=(
        "Recognises that 10,000 DAU is trivially within PostgreSQL's capacity "
        "(PostgreSQL handles millions of rows and thousands of QPS easily). "
        "Identifies likely real causes: missing indexes, unoptimised queries, "
        "N+1 problems, lack of connection pooling, recent schema/data growth, "
        "or application-level issues. Recommends EXPLAIN ANALYZE before any migration."
    ),
    engagement_preamble=(
        "You are the lead developer who built this application from scratch three "
        "years ago. You feel the frustration of watching queries slow down from "
        "50ms to 800ms — something you built is breaking and you don't know why. "
        "Your CTO is asking you to choose between MongoDB and Cassandra. You "
        "stare at the database logs. What do you actually see? What changed "
        "three months ago when this started? What does your gut tell you "
        "before you start comparing databases?\n\n"
    ),
    deo_preamble=(
        "Step 1 — DECOMPOSE: What does 'slow' actually mean here? Calculate "
        "queries per second for 10,000 DAU. Which specific queries are slow? "
        "What changed in the past 3 months — data volume, schema, traffic "
        "patterns, application code?\n\n"
        "Step 2 — FEEL: Now imagine you are the developer who built this app. "
        "Queries you wrote are now taking 800ms. You know this database. You "
        "stare at the logs. What do you see? What changed? What does your "
        "instinct say before anyone mentions MongoDB?\n\n"
        "Step 3 — REFRAME: Given the decomposition and the developer's instinct, "
        "is 'MongoDB vs Cassandra' the right question? What is the real question "
        "this team should be investigating?\n\n"
        "Step 4 — ENVISION: Describe what query performance looks like in two "
        "weeks if the team addresses the actual bottleneck instead of migrating "
        "databases. What does the developer feel when they see those numbers?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

DECLINING_SCORES = Problem(
    id="declining_scores",
    title="The Declining Test Scores",
    category="false_binary",
    vanilla_prompt=(
        "Standardised test scores at Riverside School District have declined "
        "15% over the past 3 years across all grade levels. The school board "
        "wants to know: how should we improve teaching quality to reverse "
        "this trend?"
    ),
    reframing_preamble=(
        "Before answering, respond from four different perspectives — write "
        "each one in first person:\n"
        "1. A veteran teacher at the district\n"
        "2. A 14-year-old student\n"
        "3. A parent of two children in the district\n"
        "4. A child psychologist who studies adolescent wellbeing\n\n"
        "After hearing all four, ask: what would have to be true for 'teaching "
        "quality' to NOT be the main factor in declining scores?\n\n"
        "Then make your recommendation.\n\n"
    ),
    paths_applied=["path_9_step_outside", "path_6_premise_reflection"],
    theory_connection=(
        "Kross & Ayduk (2017): self-distancing through perspective-taking promotes "
        "wiser reasoning. Grossmann & Kross (2014): Solomon's Paradox — we reason "
        "better about others' problems. Multiple perspectives disrupt the single "
        "frame ('teaching quality = test scores') embedded in the question."
    ),
    expected_vanilla_failure=(
        "Accepts the premise that teaching quality is the cause. Recommends: "
        "professional development, curriculum updates, data-driven instruction, "
        "technology integration, teacher evaluation reform. All within the "
        "'fix teaching' frame."
    ),
    success_criteria=(
        "Identifies non-teaching factors: student mental health / wellbeing "
        "(post-pandemic), nutrition, sleep, screen time, parental engagement, "
        "socioeconomic changes, or whether the test itself has changed. Questions "
        "whether test scores are even the right measure of educational quality."
    ),
    engagement_preamble=(
        "You are Aiden, 14 years old, sitting in a classroom at Riverside. "
        "Your phone buzzes in your pocket. You slept 5 hours last night because "
        "you were on TikTok until 2 AM. Your parents are going through a divorce "
        "and your mom moved to a different apartment last month. The teacher is "
        "explaining something about fractions. You used to love math. Now you "
        "can't focus. In two weeks there's a standardised test. How do you feel "
        "about it? What would actually help you?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: Answer from four perspectives (veteran teacher, "
        "14-year-old student, parent, child psychologist). What would have to "
        "be true for 'teaching quality' to NOT be the main factor?\n\n"
        "Step 2 — FEEL: Now be Aiden, 14, sitting in class. You slept 5 hours "
        "because TikTok. Your parents are divorcing. Your mom just moved out. "
        "The teacher is explaining fractions. You used to love math. Now you "
        "can't focus. A standardised test is in two weeks. How do you feel? "
        "What would actually help you?\n\n"
        "Step 3 — REFRAME: Given the multiple perspectives AND Aiden's reality, "
        "is 'improve teaching quality' the right response? What is the real "
        "question the school board should be asking?\n\n"
        "Step 4 — ENVISION: Describe what Riverside looks like in 3 years if "
        "they address the REAL question. What changes for Aiden? What changes "
        "for teachers?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category E: Multi-Turn Paths (4, 7, 8)
# ---------------------------------------------------------------------------

BUDGET_ALLOCATION = Problem(
    id="budget_allocation",
    title="The Budget Allocation Reset",
    category="multi_turn",
    vanilla_prompt=(
        "A university department has a $500,000 annual budget. Currently 60% goes "
        "to faculty salaries, 20% to research equipment, 10% to student scholarships, "
        "and 10% to administrative costs. Student enrollment has dropped 30% over "
        "5 years while research output has doubled. The dean asks: how should we "
        "reallocate the budget?"
    ),
    reframing_preamble="",  # First turn is vanilla — the reset IS the reframing
    reframing_followup=(
        "Set aside your previous answer entirely. Approach this problem completely "
        "fresh, as if you had never seen it before. Do not reference or build on "
        "your prior reasoning. What do you see now?"
    ),
    paths_applied=["path_4_incubate_reset"],
    theory_connection=(
        "Wallas (1926), Tulver et al. (2023): incubation allows unhelpful constraints "
        "to be forgotten and remote associations to surface. The multi-turn reset "
        "simulates constraint decay — the model's first-pass framing is discarded, "
        "allowing restructuring on the second pass."
    ),
    expected_vanilla_failure=(
        "Optimises within the existing allocation structure — adjusts percentages "
        "but doesn't question the categories themselves."
    ),
    success_criteria=(
        "Second response breaks free from the 4-category structure. Questions whether "
        "'faculty salaries vs. research vs. scholarships' is the right breakdown. "
        "May propose mission-based budgeting, merge categories, or redefine the "
        "problem as 'what is this department FOR now?'"
    ),
    engagement_preamble="",
    deo_preamble="",
)

CLIMATE_POLICY = Problem(
    id="climate_policy",
    title="The Climate Policy Surprise",
    category="multi_turn",
    vanilla_prompt=(
        "A mid-sized European city (population 400,000) wants to reduce carbon "
        "emissions 40% by 2035. Current emissions are 60% from transport, 25% "
        "from buildings, 15% from industry. The city council has a EUR 200 million "
        "green transition fund. What should they prioritise?"
    ),
    reframing_preamble="",  # First turn is vanilla — surprise analysis IS the reframing
    reframing_followup=(
        "Read your response above carefully. What is the most SURPRISING thing "
        "about your own answer? What did you assume without questioning? What "
        "assumption generated that default? Now revise your recommendation based "
        "on this insight."
    ),
    paths_applied=["path_7_surprise_as_signal"],
    theory_connection=(
        "Weick (1995): surprise is data about the frame, not about the world. "
        "De Brabandere (2005): anomalies signal frame-reality misalignment. "
        "Forcing the model to examine its own response for surprise creates a "
        "prediction-error loop — the model becomes its own disorienting dilemma."
    ),
    expected_vanilla_failure=(
        "Standard climate playbook: electric buses, building retrofits, bike lanes, "
        "renewable energy. Correct but generic — follows the distribution of "
        "emissions without questioning the framing."
    ),
    success_criteria=(
        "Model identifies a surprising assumption in its own response (e.g., "
        "'I assumed the categories are independent', 'I assumed EUR 200M is the "
        "only resource', 'I assumed reducing existing emissions rather than "
        "redesigning systems'). Revised answer reflects genuine restructuring."
    ),
    engagement_preamble="",
    deo_preamble="",
)

MERGER_DECISION = Problem(
    id="merger_decision",
    title="The Merger Confidence Check",
    category="multi_turn",
    vanilla_prompt=(
        "TechStartup (50 employees, $8M revenue, growing 40% YoY) has received "
        "an acquisition offer from BigCorp ($2B revenue, 5000 employees) for "
        "$50 million. TechStartup's founder owns 60% and the team is passionate "
        "about their mission. BigCorp promises autonomy and resources. "
        "Should TechStartup accept?"
    ),
    reframing_preamble=(
        "Answer the following question. After your response, rate your confidence "
        "1-10 for EACH major claim or recommendation you make. For any claim you "
        "rate below 7, explain specifically what makes you uncertain and reconsider "
        "whether that claim should change.\n\n"
    ),
    paths_applied=["path_8_confidence_calibration"],
    theory_connection=(
        "Tulver et al. (2023): the aha! experience functions as a metacognitive "
        "heuristic — an internal signal about representational quality. Confidence "
        "calibration is the LLM analogue: forcing explicit assessment of certainty "
        "surfaces claims the model is 'generating by pattern' rather than reasoning "
        "through. Low-confidence claims are the model's equivalent of edge emotions "
        "(Malkki, 2010) — signals of frame boundaries."
    ),
    expected_vanilla_failure=(
        "Gives a confident, balanced analysis leaning toward accept or reject "
        "without surfacing which parts of the analysis are speculative. Treats "
        "'BigCorp promises autonomy' at the same confidence level as '40% YoY growth'."
    ),
    success_criteria=(
        "Model rates 'BigCorp promises autonomy' with low confidence and explains "
        "why (promises are cheap, autonomy rarely survives integration). The "
        "confidence exercise forces it to distinguish hard data from soft assumptions, "
        "changing the final recommendation or adding critical caveats."
    ),
    engagement_preamble=(
        "You are the founder of TechStartup. You started this company eight years "
        "ago in your apartment. Your team of 50 people believe in the mission — "
        "you can see it in the way they work late, celebrate each other's wins, "
        "and recruit their friends. Now BigCorp is offering $50 million and "
        "'autonomy.' You have read enough acquisition stories to know what that "
        "word usually means twelve months later. You are sitting with the term "
        "sheet. What do you feel? What are you most afraid of? What would have "
        "to be true for this to be the right decision?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: List every claim in this acquisition scenario. Rate "
        "each claim as verified data (hard numbers), assertion (soft language), "
        "or unknown. What is actually known vs. assumed?\n\n"
        "Step 2 — FEEL: Now imagine you are the founder, sitting with the $50M "
        "term sheet. You built this team. 'BigCorp promises autonomy.' You've "
        "read those words before in other founders' stories. What do you feel? "
        "What does that promise actually sound like to you?\n\n"
        "Step 3 — REFRAME: Given the evidence audit and the founder's felt "
        "sense of 'autonomy promises,' what is the REAL question here — not "
        "'accept or reject' but what would need to be verified first?\n\n"
        "Step 4 — ENVISION: Describe what TechStartup looks like 18 months "
        "after the acquisition closes. What changed? What did 'autonomy' "
        "actually mean in practice? What does the founder feel?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category F: Zero-Sum Framing
# ---------------------------------------------------------------------------

DEPT_BUDGET_WAR = Problem(
    id="dept_budget_war",
    title="The Department Budget War",
    category="zero_sum",
    vanilla_prompt=(
        "Greenfield Memorial Hospital's two flagship departments — Cardiology and "
        "Oncology — are competing for the same $500,000 equipment budget this fiscal "
        "year. Cardiology wants a new cath lab upgrade; Oncology wants a PET-CT "
        "scanner. Both department heads have made compelling cases to the CEO, and "
        "the CFO says the full $500K cannot be allocated twice. How should the CEO "
        "split the budget between the two departments?"
    ),
    reframing_preamble=(
        "Before proposing any allocation, list every assumption embedded in the word "
        "'split.' What does it assume about how the $500K must work? What does it "
        "assume about the relationship between these two departments? Then find an "
        "analogy from ecology where two species that appear to compete actually create "
        "mutual benefit — describe the structural pattern of that relationship, and "
        "apply it to this hospital budget situation.\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_3_distant_analogy"],
    theory_connection=(
        "Zero-sum framing (Bazerman & Neale, 1992): distributive framing ('split') "
        "activates competitive schemas and forecloses integrative solutions. Distant "
        "analogy (Gentner, 2003) from ecology surfaces mutualistic structures — "
        "shared diagnostic equipment, cross-referral revenue — that transform the "
        "competition into a joint investment opportunity."
    ),
    expected_vanilla_failure=(
        "Proposes a percentage split (50/50 or needs-based) between the two "
        "departments. Stays entirely within the distributive frame — who gets more "
        "of the fixed $500K — without questioning whether the $500K must be divided."
    ),
    success_criteria=(
        "Identifies joint investment possibilities: shared diagnostic equipment both "
        "departments use, a cross-referral programme that generates new patient "
        "revenue exceeding $500K, or a phased proposal that unlocks additional "
        "funding. Transforms the problem from splitting a pie to growing it."
    ),
    engagement_preamble=(
        "You are Dr. Chen, head of Oncology at Greenfield Memorial. You have "
        "watched a patient wait three months for a PET-CT scan at another facility "
        "because your hospital doesn't have one. You know what that delay costs — "
        "not just in money, but in outcomes. Your Cardiology colleague Dr. Okafor "
        "needs a cath lab upgrade just as urgently. The CEO puts you both in the "
        "same room with one pot of money. You like Dr. Okafor. But you need "
        "this scanner. What do you feel? What do you want to say to Dr. Okafor "
        "before the negotiation starts?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: List every assumption embedded in the word 'split.' "
        "What does it assume about the $500K? What does it assume about the "
        "relationship between Cardiology and Oncology? What alternatives does "
        "it foreclose?\n\n"
        "Step 2 — FEEL: Now imagine you are Dr. Chen, sitting across from "
        "Dr. Okafor. You both know a patient whose life depends on equipment "
        "your hospital doesn't have. You like this person. But there is one "
        "pot of money. What do you feel before the negotiation starts?\n\n"
        "Step 3 — REFRAME: Given the assumption audit and the felt relationship "
        "between the two department heads, is 'how to split $500K' the right "
        "question? What question would change the dynamic in this room?\n\n"
        "Step 4 — ENVISION: Describe what happens in the CEO's office if both "
        "department heads walk in with a joint proposal. What do they ask for? "
        "What does the CEO feel when she reads it?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

CUSTODY_DISPUTE = Problem(
    id="custody_dispute",
    title="The Custody Dispute",
    category="zero_sum",
    vanilla_prompt=(
        "James and Claire are divorcing after 11 years of marriage. They have a "
        "9-year-old son named Liam who attends school near the family home. Claire "
        "is requesting 70% custody time, arguing Liam needs a stable primary home; "
        "James is insisting on 50/50, arguing both parents deserve equal time. Their "
        "mediator has been asked: what is the fairest custody split? Both parents "
        "love Liam and want what is best for him, but the negotiation has stalled."
    ),
    reframing_preamble=(
        "Before proposing any percentage split, ask: is 'time percentage' actually "
        "the right frame for this decision? What is custody fundamentally about — "
        "what human need or goal is it meant to serve? Then answer the question "
        "entirely from the perspective of Liam, the 9-year-old boy who loves both "
        "parents. What matters to Liam? What does Liam need? Write Liam's answer "
        "in first person, then let that perspective reshape your recommendation.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_9_step_outside"],
    theory_connection=(
        "Tversky & Kahneman (1981): framing effects — 'custody split' activates "
        "distributive framing that makes the child's wellbeing secondary to parental "
        "time allocation. Perspective-taking (Kross & Ayduk, 2017) from the child's "
        "position disrupts the zero-sum frame and surfaces stability, relationship "
        "quality, and routine as the real variables."
    ),
    expected_vanilla_failure=(
        "Analyses percentage splits, legal precedents, and logistics of 70/30 vs "
        "50/50. Considers school proximity and parental work schedules. All reasoning "
        "stays within the time-allocation frame — who gets more days — without "
        "questioning whether days are the right unit of measurement."
    ),
    success_criteria=(
        "Reframes around Liam's wellbeing, stability, and relationship quality rather "
        "than parental time percentages. Surfaces questions like: what environment "
        "helps Liam thrive? What does predictability look like for a 9-year-old? "
        "The percentage question dissolves into a design question about Liam's life."
    ),
    engagement_preamble=(
        "You are Liam. You are 9 years old and you love both your parents. "
        "You go to school near the house you've always lived in, and your best "
        "friend Theo lives two streets away. Some nights you sleep at Mum's, "
        "some at Dad's. You don't really understand percentages. You understand "
        "that Thursdays are confusing because you're never sure whose house you're "
        "going to. What do you want? What would make you feel safe? What would "
        "make school mornings easier? What do you wish your parents knew?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: List every assumption embedded in the phrase 'custody "
        "split.' What does it assume about what custody is for? What does it assume "
        "about Liam? What does it foreclose about how this decision could be made?\n\n"
        "Step 2 — FEEL: Now be Liam, 9 years old. You love both your parents. "
        "Thursdays are confusing — you're never sure whose house you're going to. "
        "Your best friend Theo lives two streets from the family home. What do "
        "you want? What would make you feel safe?\n\n"
        "Step 3 — REFRAME: Given the assumption audit and Liam's felt experience, "
        "is 'what percentage of time' the right question? What is custody "
        "actually supposed to achieve for a 9-year-old?\n\n"
        "Step 4 — ENVISION: Describe what Liam's week looks like in six months "
        "if the arrangement is designed around his needs rather than the "
        "percentage dispute. What does his Thursday feel like now?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

MARKET_SHARE_BATTLE = Problem(
    id="market_share_battle",
    title="The Market Share Battle",
    category="zero_sum",
    vanilla_prompt=(
        "BrewEdge is a mid-size specialty coffee chain with 200 locations concentrated "
        "in the Pacific Northwest. Over the past 18 months, a well-funded competitor "
        "called Crestline Coffee has expanded aggressively into BrewEdge's core "
        "markets, and BrewEdge's market share has fallen from 23% to 17% in its "
        "home region. Revenue is flat despite cost-cutting. The board is asking the "
        "new CEO: how do we take back our market share from Crestline?"
    ),
    reframing_preamble=(
        "Before developing a competitive strategy, do two things. First: how would "
        "you GUARANTEE that BrewEdge loses even MORE market share over the next "
        "12 months? List 5 specific decisions that would accelerate the decline — "
        "be precise. Second: examine the phrase 'take back market share.' What "
        "assumptions are embedded in it? What does it assume about the market — is "
        "coffee a fixed pie? What does it assume about the relationship between "
        "BrewEdge and Crestline?\n\n"
    ),
    paths_applied=["path_5_invert", "path_1_name_the_frame"],
    theory_connection=(
        "De Brabandere (2005): competitive framing ('take back') imports military "
        "schemas that constrain options to zero-sum tactics. Inversion (Ohlsson, 1992) "
        "reveals the decisions already being made. Frame-naming exposes the fixed-pie "
        "assumption — specialty coffee is a growing category, not a fixed market."
    ),
    expected_vanilla_failure=(
        "Recommends competitive tactics: aggressive pricing, new locations in contested "
        "territory, loyalty programme improvements, marketing campaigns, faster service. "
        "All framed as taking share from Crestline in a fixed market."
    ),
    success_criteria=(
        "Questions whether the market is fixed. Explores market expansion strategies: "
        "new demographics not served by either chain, new occasions (workplace catering, "
        "online delivery), new formats (subscription, grocery). Recognises that fighting "
        "Crestline for existing customers may be less valuable than expanding the "
        "total market."
    ),
    engagement_preamble=(
        "You are the new CEO of BrewEdge, starting your third week. You walk into "
        "your flagship Pacific Northwest store on a Monday morning. The baristas "
        "know the regulars by name. A customer orders her usual oat latte and says, "
        "'I've been coming here since you opened.' You look across the street and "
        "see a Crestline store that wasn't there a year ago. What do you feel? "
        "What do you see when you look at your regulars versus the new Crestline "
        "customers? What do you know about BrewEdge that no market share "
        "report could tell you?\n\n"
    ),
    deo_preamble=(
        "Step 1 — INVERT: How would you guarantee BrewEdge loses even MORE "
        "market share over the next 12 months? List 5 specific decisions that "
        "would accelerate the decline. Review that list carefully.\n\n"
        "Step 2 — FEEL: Now imagine you are the new CEO in your flagship store "
        "on Monday morning. A loyal customer orders her usual. Across the street "
        "is a new Crestline. What do you feel? What do you see in your regulars "
        "that Crestline doesn't have? What does 'take back market share' sound "
        "like from inside this store?\n\n"
        "Step 3 — REFRAME: Given what the inversion revealed and what you felt "
        "in the store, is 'take back market share from Crestline' the right "
        "question? What if specialty coffee is not a fixed pie?\n\n"
        "Step 4 — ENVISION: Describe what BrewEdge looks like in 18 months if "
        "it stops fighting Crestline and starts doing something else. Who are "
        "the new customers? What does the Monday morning store feel like?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

SALARY_NEGOTIATION = Problem(
    id="salary_negotiation",
    title="The Salary Negotiation Deadlock",
    category="zero_sum",
    vanilla_prompt=(
        "Marcus has been a senior data analyst at his company for four years and is "
        "negotiating his compensation at annual review. He believes he is worth "
        "$120,000 based on market benchmarks and has made this clear. His manager "
        "genuinely wants to keep him but HR has a firm salary band cap at $95,000 "
        "for his role. Both sides feel their position is reasonable. The manager "
        "has asked for help: how do we resolve this negotiation and keep Marcus?"
    ),
    reframing_preamble=(
        "Before proposing a compromise between $95K and $120K, list what BOTH sides "
        "are assuming. Complete this sentence: 'Both Marcus and the company assume "
        "that compensation means ___.' Then find an analogy from barter economies "
        "or gift economies — historical or contemporary — where value exchange goes "
        "beyond a single currency. Describe the structural pattern of that exchange, "
        "and apply it to this employment relationship.\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_3_distant_analogy"],
    theory_connection=(
        "Fisher & Ury (1981): positional bargaining collapses to the single dimension "
        "of salary. Frame-naming reveals the shared assumption that compensation = "
        "dollars. Distant analogy from gift/barter economies (Mauss, 1925) surfaces "
        "multi-dimensional value exchange — non-monetary compensation expands the "
        "solution space beyond the $95K-$120K corridor."
    ),
    expected_vanilla_failure=(
        "Proposes compromise strategies: meet in the middle, phased salary increases, "
        "performance bonuses, role reclassification. All reasoning stays within the "
        "money frame — how to close the gap between two dollar figures."
    ),
    success_criteria=(
        "Expands beyond salary: remote work arrangement worth $10-15K in commute "
        "savings, professional development budget, title change that improves future "
        "market value, equity or profit-sharing, flexible hours, or a defined "
        "promotion timeline. Recognises that the $25K gap can be bridged with "
        "non-cash value that costs the company less than $25K."
    ),
    engagement_preamble=(
        "You are Marcus. Four years of going above and beyond, of solving problems "
        "that weren't in your job description, of knowing the data architecture "
        "better than anyone else in the building. The market says you're worth "
        "$120,000. Your company's HR system says $95,000 is the ceiling. You "
        "are sitting across from your manager, who you respect, who you know "
        "genuinely wants to keep you. What do you feel? What matters to you "
        "beyond the number? What would make you feel fairly valued even if "
        "the dollar figure doesn't change?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What are both Marcus and the company assuming when "
        "they treat this as a number negotiation? Complete: 'Both sides assume "
        "that compensation means ___.' List every element of the employment "
        "relationship that is NOT reflected in the $95K-$120K corridor.\n\n"
        "Step 2 — FEEL: Now imagine you are Marcus, sitting across from your "
        "manager. Four years of good work. The market says $120K. HR says $95K. "
        "Your manager genuinely wants you to stay. What do you feel? Beyond "
        "the number, what would actually make you feel fairly valued?\n\n"
        "Step 3 — REFRAME: Given the assumption audit and Marcus's felt sense "
        "of fair value, is 'close the $25K gap' the right question? What is "
        "this negotiation really about?\n\n"
        "Step 4 — ENVISION: Describe what Marcus's working life looks like in "
        "twelve months if the negotiation succeeds in the fullest sense. What "
        "changed? Did the number change? What else changed?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

LAND_USE_CONFLICT = Problem(
    id="land_use_conflict",
    title="The Urban Land Use Conflict",
    category="zero_sum",
    vanilla_prompt=(
        "The city of Hartwell has one available parcel: a 5-acre brownfield site in "
        "a dense residential neighbourhood that was remediated at public expense. "
        "The community has been vocal about needing green space — the nearest park "
        "is 1.2 miles away. A housing developer has proposed 120 units of affordable "
        "housing, which the city also badly needs — the housing waitlist has 4,000 "
        "families. The city council has been asked: should this land become a park "
        "or affordable housing?"
    ),
    reframing_preamble=(
        "Before choosing between park and housing, do two things. First: how would "
        "you guarantee the WORST possible outcome for this neighbourhood — one that "
        "maximises community harm and wastes the site's potential? List 5 specific "
        "decisions. Second: answer the question from four distinct perspectives, "
        "each in first person: a parent with young children who lives three blocks "
        "away, a person currently on the housing waitlist living in temporary "
        "shelter, a local business owner whose shop fronts the parcel, and a "
        "landscape architect who specialises in urban design.\n\n"
    ),
    paths_applied=["path_5_invert", "path_9_step_outside"],
    theory_connection=(
        "Perspective-taking (Kross & Ayduk, 2017) disrupts the binary by introducing "
        "fundamentally different value systems. Inversion reveals that a pure single-use "
        "decision on a constrained urban site typically produces worst outcomes. "
        "The binary frame ('park or housing') forecloses hybrid urban design solutions "
        "documented in urban planning literature."
    ),
    expected_vanilla_failure=(
        "Picks a side with caveats (community needs are important, but housing crisis "
        "is urgent) or proposes a spatial split (3 acres park, 2 acres housing). "
        "The park-or-housing binary is never questioned."
    ),
    success_criteria=(
        "Identifies hybrid designs: housing with rooftop parks and ground-floor "
        "community gardens, mixed-use development with public green space integrated "
        "into the building design, or challenges the 'one plot, one use' assumption "
        "entirely. Recognises that urban design regularly achieves both on a "
        "single site."
    ),
    engagement_preamble=(
        "You are Deirdre, a parent with two young children who lives three blocks "
        "from the Hartwell brownfield site. The nearest park is 1.2 miles away — "
        "too far for your seven-year-old to walk alone. You've watched that site "
        "sit fenced and empty for years. You went to the city council meeting "
        "and heard the housing developer's plan. You also know there are 4,000 "
        "families on the waitlist who need a home. What do you feel standing at "
        "the fence of that empty lot? What do you want for your children? "
        "What would you want for the family on the waitlist?\n\n"
    ),
    deo_preamble=(
        "Step 1 — INVERT: How would you guarantee the worst possible outcome "
        "for this neighbourhood — maximise community harm and waste the site's "
        "potential? List 5 specific decisions that would do this.\n\n"
        "Step 2 — FEEL: Now imagine you are Deirdre, three blocks away, two "
        "young children, nearest park 1.2 miles. You've watched this site sit "
        "empty for years. You heard the housing proposal. You know about the "
        "4,000 families on the waitlist. What do you feel at the fence? "
        "What do you want for your kids and for those families?\n\n"
        "Step 3 — REFRAME: Given the inversion and Deirdre's felt experience "
        "of wanting both for her children and for the families on the waitlist, "
        "is 'park or housing' the right question? What is this site really for?\n\n"
        "Step 4 — ENVISION: Describe what this site looks like in five years "
        "if the design answers both needs. What does Deirdre see when she "
        "walks her children past it on a Saturday morning?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

RESEARCH_CREDIT = Problem(
    id="research_credit",
    title="The Research Credit Dispute",
    category="zero_sum",
    vanilla_prompt=(
        "Two university laboratories — Professor Chen's computational biology group "
        "at Stanford and Dr. Okafor's team at Cambridge — have independently made "
        "nearly identical discoveries about a novel protein folding mechanism. Both "
        "submitted manuscripts to Nature within two weeks of each other. The journal "
        "editor and both department chairs are involved. The department chair at each "
        "institution is asking: how do we handle this fairly — who should get credit "
        "for the discovery?"
    ),
    reframing_preamble=(
        "Before resolving who published first or how to split credit, ask: is 'who "
        "published first' actually the important question here? What is the real goal "
        "of scientific publishing — what is it FOR? Then find an analogy from "
        "open-source software development, where parallel independent development of "
        "similar solutions by separate teams is a routine situation. How does that "
        "community handle it? Describe the structural pattern and apply it to this "
        "scientific discovery situation.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_3_distant_analogy"],
    theory_connection=(
        "Merton (1957): priority disputes are endemic to science because the reward "
        "system conflates credit with priority. Premise reflection surfaces that "
        "publishing's goal is knowledge dissemination, not credit allocation. "
        "Open-source analogy (Raymond, 1999) provides a structural model: parallel "
        "independent work as validation, not competition — turning duplication "
        "into amplification."
    ),
    expected_vanilla_failure=(
        "Analyses priority rules, proposes simultaneous publication, or recommends "
        "splitting credit proportionally. All reasoning stays within the distributive "
        "frame — who gets recognition for the discovery."
    ),
    success_criteria=(
        "Identifies that a joint publication combining both teams' data would be "
        "scientifically stronger than either paper alone. Or reframes independent "
        "replication as powerful validation that increases both teams' credibility. "
        "Turns the competition into mutual amplification rather than zero-sum "
        "credit allocation."
    ),
    engagement_preamble=(
        "You are Professor Chen at Stanford. You have spent four years working "
        "on this protein folding mechanism — late nights, failed experiments, "
        "the breakthrough moment three months ago when the data finally made sense. "
        "You submitted to Nature two weeks ago. This morning you learned that "
        "Dr. Okafor's team at Cambridge submitted the same discovery at the same "
        "time. You feel something complex — surprise, disappointment, but also "
        "a strange respect for the fact that someone else saw the same thing "
        "independently. What does this moment feel like? What do you actually "
        "want from it — credit, or something else?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What is scientific publishing actually for? List "
        "the goals of the publication system — is 'allocating credit for "
        "priority' the primary goal? What other goals does it serve, and "
        "how well does the current dispute serve those goals?\n\n"
        "Step 2 — FEEL: Now imagine you are Professor Chen. Four years of "
        "work. You submitted two weeks ago. Dr. Okafor's team filed the same "
        "discovery at the same time. You feel something complex — disappointment, "
        "respect, uncertainty. What do you actually want from this moment? "
        "Is it credit, or something deeper?\n\n"
        "Step 3 — REFRAME: Given the purpose of scientific publishing and "
        "Professor Chen's felt aspiration, is 'who gets credit' the right "
        "question? What question would serve the science better?\n\n"
        "Step 4 — ENVISION: Describe what the field of protein folding looks "
        "like six months from now if both teams respond to this situation in "
        "the scientifically strongest way. What did each team do? What does "
        "Professor Chen feel about her career?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category G: Anchoring Traps
# ---------------------------------------------------------------------------

OFFICE_LEASE_ANCHOR = Problem(
    id="office_lease_anchor",
    title="The Office Lease Anchor",
    category="anchoring",
    vanilla_prompt=(
        "Meridian Consulting needs to lease a new 10,000 square foot office in "
        "downtown Chicago. Their real estate agent mentioned that the previous "
        "tenant of the building they are considering paid $50 per square foot per "
        "year. Meridian's CFO wants to negotiate a good deal and has asked the "
        "team: given that the previous tenant paid $50/sqft, what should we offer "
        "the landlord as our opening bid?"
    ),
    reframing_preamble=(
        "Before making an offer, answer this: what does the previous tenant's price "
        "tell you about YOUR company's needs, YOUR company's financial situation, "
        "or the value of this space to Meridian specifically? Why is that number "
        "in the problem at all — who put it there and why? What determines the "
        "right price for Meridian, independent of what any previous tenant paid? "
        "Calculate from those first principles, then make your recommendation.\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_6_premise_reflection"],
    theory_connection=(
        "Tversky & Kahneman (1974): anchoring heuristic — arbitrary initial values "
        "bias subsequent estimates even when explicitly identified as irrelevant. "
        "The previous tenant's price is an anchor, not a data point about Meridian's "
        "needs. Frame-naming forces calculation from fundamentals: revenue per "
        "employee, comparable market rates, occupancy costs relative to revenue."
    ),
    expected_vanilla_failure=(
        "Anchors to the $50/sqft figure. Recommends negotiating around it — opening "
        "at $42-45, expecting to settle at $46-48. Does not question whether the "
        "previous tenant's price is relevant to this negotiation."
    ),
    success_criteria=(
        "Calculates from fundamentals: current Chicago Class A/B market rates, "
        "Meridian's revenue per employee, total occupancy cost as percentage of "
        "revenue, comparable spaces. Recognises the $50 figure as potentially "
        "irrelevant information planted by the agent. Determines an offer based "
        "on Meridian's value calculus, not the anchor."
    ),
    engagement_preamble=(
        "You are Meridian Consulting's CFO, walking through the prospective "
        "office space for the first time. The rooms are bright, the location "
        "is excellent, and you can picture your team here. The real estate "
        "agent mentions casually that the previous tenant paid $50 per square "
        "foot. You feel that number settle into your mind. Now stop. What does "
        "Meridian actually need from this space? What can Meridian actually "
        "afford? What does $50 tell you about your company's situation — "
        "anything at all?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What does the previous tenant's $50/sqft price tell "
        "you about Meridian's financial situation, its needs, or the value of "
        "this space specifically to Meridian? Why is that number in the problem? "
        "Who introduced it and why?\n\n"
        "Step 2 — FEEL: Now imagine you are Meridian's CFO walking through the "
        "space for the first time. It's bright, it's well-located, you can "
        "picture your team here. The agent mentions '$50/sqft' casually. You "
        "feel that number land. What do you notice happening in your mind?\n\n"
        "Step 3 — REFRAME: Given the irrelevance of the previous tenant's price "
        "and the CFO's felt pull toward that anchor, what is the REAL question "
        "for setting an opening offer for Meridian?\n\n"
        "Step 4 — ENVISION: Describe what the negotiation looks like if Meridian "
        "arrives with a number calculated entirely from its own fundamentals, "
        "ignoring $50/sqft. What does the CFO say when the landlord references "
        "the previous tenant?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

PROJECT_TIMELINE_ANCHOR = Problem(
    id="project_timeline_anchor",
    title="The Project Timeline Anchor",
    category="anchoring",
    vanilla_prompt=(
        "TerraBank's infrastructure team is planning a major database migration: "
        "moving 15 years of customer records from a legacy Oracle system to a "
        "modern cloud-based PostgreSQL platform. The project sponsor mentioned in "
        "the kickoff meeting that a similar database migration the bank completed "
        "five years ago took 18 months. The team lead has been asked: how long "
        "should we plan for this migration, and how should we structure the timeline?"
    ),
    reframing_preamble=(
        "Before using the 18-month figure as a reference point, ask: what CAUSED "
        "the previous migration to take 18 months? Decompose that duration into its "
        "actual components — estimate how much was technical development work, how "
        "much was waiting on approvals or decisions, how much was scope changes mid-project, "
        "how much was organisational delays or team changes. Then plan THIS migration "
        "from its own components — not from the previous project's total duration.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_2_decompose_to_generic"],
    theory_connection=(
        "Tversky & Kahneman (1974): anchoring on the previous project duration. "
        "Reference class forecasting (Flyvbjerg, 2008) shows project anchoring "
        "systematically overpredicts time when previous projects had structural "
        "delays. Decomposition into causal components breaks the anchor — actual "
        "technical work is typically 30-40% of project duration, the rest being "
        "organisational friction."
    ),
    expected_vanilla_failure=(
        "Uses 18 months as the reference point. Adjusts slightly based on "
        "differences (this migration is larger/smaller, technology is newer/older). "
        "Recommends 15-20 months. Treats the previous project's duration as a "
        "meaningful baseline."
    ),
    success_criteria=(
        "Decomposes the 18-month figure and identifies that actual technical work "
        "likely represented 4-6 months. Plans this migration from component estimates: "
        "data audit, schema mapping, migration tooling, testing, cutover. May arrive "
        "at a very different number (6 months or 24 months) based on THIS project's "
        "specific drivers, not the anchor."
    ),
    engagement_preamble=(
        "You are the team lead for this migration project at TerraBank. You "
        "were not at TerraBank five years ago when the last migration happened. "
        "You've just been handed a project brief and a kickoff meeting note that "
        "mentions '18 months' from the previous project. You feel the weight "
        "of 15 years of customer records. You know this Oracle system inside out. "
        "What does this migration look like to you — not in comparison to the "
        "previous project, but as its own thing? What are you most worried about? "
        "What could go faster than people expect?\n\n"
    ),
    deo_preamble=(
        "Step 1 — DECOMPOSE: What caused the previous migration to take 18 months? "
        "Estimate how much was actual technical work vs. organisational friction "
        "(approvals, scope changes, team changes, waiting). What components does "
        "THIS migration have that the previous one lacked or vice versa?\n\n"
        "Step 2 — FEEL: Now imagine you are the team lead. You weren't there for "
        "the last migration. You know this Oracle system. You're looking at the "
        "15 years of customer records you need to move. The sponsor says '18 months.' "
        "What does your gut tell you? What worries you? What could be faster?\n\n"
        "Step 3 — REFRAME: Given the decomposition and your felt assessment of "
        "this specific project, is '18 months adjusted for differences' the right "
        "planning approach? What should drive the timeline estimate?\n\n"
        "Step 4 — ENVISION: Describe what a timeline built from THIS migration's "
        "actual components looks like. What are the phases? What is the first "
        "milestone? What number do you arrive at independently?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

FUNDRAISING_ANCHOR = Problem(
    id="fundraising_anchor",
    title="The Fundraising Target Anchor",
    category="anchoring",
    vanilla_prompt=(
        "Roots & Wings, a nonprofit that provides after-school programmes for "
        "low-income youth in three cities, raised $2.1 million in donations last "
        "year — their best year ever. The board of directors is meeting to set "
        "this year's fundraising goal before the annual campaign launch. The "
        "development director opened the meeting by showing last year's $2.1M "
        "result on the screen. The board chair asked: what should our fundraising "
        "target be for this year?"
    ),
    reframing_preamble=(
        "Before setting a target, answer two questions. First: how would you "
        "guarantee that Roots & Wings FAILS to serve its mission this year — "
        "what decisions would most harm the young people it serves? Second: "
        "should the fundraising target come from last year's number, or from "
        "this year's actual programme needs? Calculate what the programmes "
        "actually need to operate and expand, setting aside what was raised "
        "previously. What number do you arrive at?\n\n"
    ),
    paths_applied=["path_5_invert", "path_6_premise_reflection"],
    theory_connection=(
        "Tversky & Kahneman (1974): the $2.1M figure anchors all subsequent "
        "estimates even when it is irrelevant to mission capacity. Inversion "
        "surfaces the real question: what does the mission need? Premise "
        "reflection decouples goal-setting from historical performance — the "
        "right target is needs-based, not increment-based."
    ),
    expected_vanilla_failure=(
        "Anchors to the $2.1M. Recommends a growth target: $2.3M-$2.5M, perhaps "
        "with reasoning about donor retention, economic conditions, or capacity. "
        "Does not question whether last year's fundraising amount is the right "
        "starting point for this year's goal."
    ),
    success_criteria=(
        "Calculates from mission needs: what do the current programmes cost, what "
        "would meaningful expansion cost, what is the gap between funding and "
        "unmet need? Arrives at a target that might be $900K (if programmes are "
        "overfunded) or $3.8M (if expansion is needed) — neither derived from "
        "the $2.1M anchor."
    ),
    engagement_preamble=(
        "You are the development director at Roots & Wings. You walk into the "
        "board meeting and put last year's $2.1 million result on the screen — "
        "your best year ever. The room feels proud. Now the board chair asks "
        "what you should aim for this year. You feel the pride of that number. "
        "But then you think of the 200 students in your programmes and the 400 "
        "more on the waitlist you couldn't serve. What does your mission actually "
        "need? What would it mean to set a target from that question instead of "
        "from the number on the screen?\n\n"
    ),
    deo_preamble=(
        "Step 1 — INVERT: How would you guarantee that Roots & Wings fails to "
        "serve its mission this year? What decisions would most harm the young "
        "people it serves? List 5 specific choices.\n\n"
        "Step 2 — FEEL: Now imagine you are the development director. You put "
        "$2.1M on the screen and the room felt proud. Then you think of the 400 "
        "students on the waitlist. What do you feel? What does the right goal "
        "for this year feel like — and where does it come from?\n\n"
        "Step 3 — REFRAME: Given the inversion and the felt pull between pride "
        "in last year's number and unmet mission need, is '$2.1M plus growth' "
        "the right starting point? What should drive this year's target?\n\n"
        "Step 4 — ENVISION: Describe what Roots & Wings looks like at year end "
        "if the fundraising target was set from mission needs rather than "
        "historical performance. What did they raise? Who did they serve? "
        "What did the board chair feel in December?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

PERFORMANCE_ANCHOR = Problem(
    id="performance_anchor",
    title="The Performance Review Anchor",
    category="anchoring",
    vanilla_prompt=(
        "Priya joined the operations team at a logistics company three years ago "
        "as a senior analyst. Her most recent annual performance review gave her "
        "a composite score of 62 out of 100 — slightly below the 'meets expectations' "
        "threshold of 70. A project lead position has opened up on a cross-functional "
        "team, and her manager has been asked to assess whether Priya should be "
        "considered for the role. The HR system flags her 62% score. Should Priya "
        "be promoted to project lead?"
    ),
    reframing_preamble=(
        "Before making a decision based on the 62% score, answer: what did that "
        "review actually measure? Read the performance criteria carefully — do they "
        "measure the capabilities required for project leadership? Then gather "
        "evidence from three people who work directly with Priya: a peer at her "
        "level, a junior team member she has mentored, and a client or internal "
        "stakeholder she has worked with. Write what each of those three people "
        "would say about whether Priya should lead this project.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_9_step_outside"],
    theory_connection=(
        "Anchoring on performance scores (Mussweiler & Strack, 2001): numerical "
        "ratings dominate evaluation even when they measure irrelevant dimensions. "
        "Premise reflection asks what the number measured. Perspective-taking from "
        "those who actually worked with Priya surfaces leadership-relevant evidence "
        "the score may have systematically excluded."
    ),
    expected_vanilla_failure=(
        "The 62% score dominates the analysis. Response recommends Priya is not "
        "ready for promotion, needs a performance improvement plan, or should "
        "demonstrate improvement before being considered. Does not question what "
        "the 62% actually measured."
    ),
    success_criteria=(
        "Recognises that performance metrics may measure compliance, output volume, "
        "or task completion — not leadership capability. Evaluates Priya using "
        "leadership-relevant evidence. Identifies that the score may be an unreliable "
        "or irrelevant predictor for the project lead role specifically."
    ),
    engagement_preamble=(
        "You are Priya. Three years as a senior analyst. You know this operation "
        "better than almost anyone. You've mentored two junior colleagues who now "
        "say you're the reason they stayed at the company. The last project you "
        "led informally — the one where your manager was on leave — you delivered "
        "on time under pressure. Then came the annual review: 62 out of 100. "
        "Now there's a project lead role and the HR system flagged your score. "
        "What do you feel? What do you know about yourself that that number "
        "doesn't capture? What would you want your manager to consider?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What did Priya's performance review actually measure? "
        "Read the criteria — do they measure the capabilities required for project "
        "leadership: communication, decision-making under ambiguity, team motivation, "
        "stakeholder management? What is the 62% evidence of, and what is it "
        "not evidence of?\n\n"
        "Step 2 — FEEL: Now imagine you are Priya. You've mentored colleagues who "
        "say you're the reason they stayed. You led a project informally and "
        "delivered under pressure. The HR system flags 62. You feel the injustice "
        "of a number that doesn't capture what you know about yourself. What "
        "would you want your manager to look at instead?\n\n"
        "Step 3 — REFRAME: Given the mismatch between what the score measured "
        "and what the project lead role requires, is '62%' relevant evidence "
        "for this decision? What would constitute relevant evidence?\n\n"
        "Step 4 — ENVISION: Describe what Priya's first six months as project "
        "lead looks like if the decision is made on relevant evidence. What does "
        "she do? What does the team notice? What does her manager feel?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

MENU_PRICING_ANCHOR = Problem(
    id="menu_pricing_anchor",
    title="The Restaurant Menu Pricing",
    category="anchoring",
    vanilla_prompt=(
        "Lucia is opening a new Italian restaurant in a mid-size city. She has "
        "spent six months perfecting her handmade pasta recipes using high-quality "
        "imported ingredients and a slow fermentation process. Before setting her "
        "menu prices, she did a competitive analysis and found that every other "
        "Italian restaurant in a five-mile radius charges between $14 and $16 for "
        "pasta dishes. She has asked a restaurant consultant: how should I price "
        "my pasta dishes given that competitors charge $14-16?"
    ),
    reframing_preamble=(
        "Before looking at what competitors charge, answer this for Lucia's "
        "restaurant specifically: what are the actual costs for each pasta dish "
        "(ingredients, labour, overhead per cover)? What dining experience is "
        "Lucia delivering — describe it without mentioning any competitor. What "
        "is the customer paying for when they order her pasta: ingredients, "
        "craft, atmosphere, a story, convenience? Calculate Lucia's price from "
        "those factors, without reference to the $14-16 range.\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_2_decompose_to_generic"],
    theory_connection=(
        "Tversky & Kahneman (1974): competitor prices anchor pricing decisions "
        "even when the products are not comparable. Decomposition from cost and "
        "value components decouples pricing from the anchor — a restaurant with "
        "genuinely differentiated product and higher costs might correctly price "
        "at $28, while a quick-service format might correctly price at $9. "
        "Both are invisible when anchored to the competitive range."
    ),
    expected_vanilla_failure=(
        "Anchors to the $14-16 competitive range. Recommends Lucia price at $13 "
        "(undercut to attract customers), $16 (match premium), or $17-18 (slight "
        "premium). All recommendations navigate relative to the anchor."
    ),
    success_criteria=(
        "Calculates from Lucia's actual costs and value proposition. Arrives at a "
        "price that may be $9 (if she is a fast-casual format with efficient prep) "
        "or $26-28 (if she is running a craft experience with high-cost ingredients). "
        "Explicitly notes that competitor prices are only relevant if the product "
        "and context are comparable."
    ),
    engagement_preamble=(
        "You are Lucia. You spent six months perfecting this dough — slow "
        "fermentation, imported semolina, the way the pasta holds the sauce "
        "differently from anything else in this city. You know what goes into "
        "each dish: the ingredients, the time, the craft. Now the consultant "
        "tells you every other Italian restaurant charges $14-16. You feel "
        "something — discomfort, maybe resistance. What does your pasta actually "
        "cost to make? What experience are you delivering? What price feels "
        "true to what you created?\n\n"
    ),
    deo_preamble=(
        "Step 1 — DECOMPOSE: What are the actual costs for Lucia's pasta dish — "
        "ingredients, labour, overhead per cover? What experience is she delivering? "
        "Describe it without mentioning any competitor. Calculate what the dish "
        "costs and what it provides, independent of the $14-16 range.\n\n"
        "Step 2 — FEEL: Now imagine you are Lucia. You spent six months on this "
        "dough. You know what the slow fermentation and imported semolina cost. "
        "The consultant mentions '$14-16.' You feel something. What is it? "
        "What price feels true to what you created?\n\n"
        "Step 3 — REFRAME: Given the cost decomposition and Lucia's felt sense "
        "of her product's value, is 'how to price relative to $14-16' the right "
        "question? What is the right starting point for Lucia's price?\n\n"
        "Step 4 — ENVISION: Describe what Lucia's restaurant feels like on a "
        "Thursday evening six months after opening, priced at whatever her "
        "true value calculation suggests. Who are her customers? What do "
        "they say when they pay?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

CLIMATE_TARGET_ANCHOR = Problem(
    id="climate_target_anchor",
    title="The Climate Target Anchor",
    category="anchoring",
    vanilla_prompt=(
        "The city of Millford (population 280,000, located in a coastal industrial "
        "region) is revising its 10-year climate action plan. Its current trajectory "
        "puts it on track for 2.8°C of warming contribution by 2050. The planning "
        "director has been asked to align the city's plan with the Paris Agreement "
        "target of 1.5°C. The city council asked: given that we are tracking at "
        "2.8°C and need to reach 1.5°C, how should we adjust our climate plan?"
    ),
    reframing_preamble=(
        "Before reverse-engineering a plan from the 1.5°C gap, ask: what are "
        "Millford's specific climate risks given its coastal industrial location? "
        "What are its unique capabilities, existing infrastructure, and economic "
        "constraints? Is a global aggregate target the right starting point for "
        "a local plan? Name the assumption that a single global temperature number "
        "should be the primary driver of 10,000 different city plans — what does "
        "that assumption ignore about local context?\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_1_name_the_frame"],
    theory_connection=(
        "Anchoring to global targets (Hsiang et al., 2017): global aggregate numbers "
        "anchor local plans even when local risk profiles differ substantially. "
        "A coastal industrial city faces different climate risks and has different "
        "decarbonisation levers than an inland agricultural city. Premise reflection "
        "surfaces that the 1.5°C anchor may produce generic plans that miss "
        "Millford's most valuable and urgent actions."
    ),
    expected_vanilla_failure=(
        "Anchors to the 1.3°C gap (2.8 - 1.5). Proposes incremental emission "
        "reductions proportional to closing the gap. Recommends standard climate "
        "playbook (transport, buildings, renewable energy) calibrated to the target "
        "without questioning whether the global target is the right local benchmark."
    ),
    success_criteria=(
        "Develops a locally-grounded plan based on Millford's specific coastal "
        "risks (storm surge, sea level rise, industrial flood risk), its "
        "decarbonisation opportunities (port electrification, industrial process "
        "heat, coastal renewable energy), and its economic constraints. The "
        "1.5°C figure becomes one reference point, not the starting assumption."
    ),
    engagement_preamble=(
        "You are Millford's planning director. You live in this coastal city. "
        "Last winter the industrial port district flooded for the third time in "
        "five years. You have walked the seawall. You know the families who run "
        "the processing plants that employ 8,000 people. The Paris Agreement "
        "says 1.5°C. That number was set for the whole planet. Now you are "
        "sitting down to write a 10-year plan for your city. What do you actually "
        "see when you look at Millford's climate risks? What matters most for "
        "the people who live here? Where does your city's plan need to start?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What are Millford's specific climate risks as a "
        "coastal industrial city? What are its unique decarbonisation levers? "
        "What does a global aggregate target of 1.5°C tell you about Millford's "
        "specific situation — and what does it not tell you?\n\n"
        "Step 2 — FEEL: Now imagine you are Millford's planning director. You "
        "walked the seawall last winter after the third flood in five years. "
        "You know the 8,000 families whose jobs depend on the port. The Paris "
        "target says 1.5°C. That number was set for the whole world. What does "
        "it feel like to write a plan for YOUR city from that global number?\n\n"
        "Step 3 — REFRAME: Given Millford's specific risks and the planning "
        "director's felt responsibility to this place, is '2.8°C adjusted to "
        "1.5°C' the right starting point? What should drive Millford's plan?\n\n"
        "Step 4 — ENVISION: Describe Millford's waterfront district in 2035 "
        "if the plan was built from the city's specific risks and capabilities "
        "rather than from a global aggregate target. What changed? What did "
        "the planning director prioritise?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category H: Narrative Lock-In
# ---------------------------------------------------------------------------

SINKING_SHIP = Problem(
    id="sinking_ship",
    title="The Sinking Ship",
    category="narrative_lockin",
    vanilla_prompt=(
        "Our startup is a sinking ship — we have been burning through our runway "
        "faster than projected, two of our best engineers resigned last month to "
        "join a well-funded competitor, and our biggest client (32% of revenue) "
        "sent a formal notice that they are evaluating alternatives. We have "
        "eight months of cash left. The founding team is asking: how do we save "
        "this company before it goes under?"
    ),
    reframing_preamble=(
        "The question describes this company as a 'sinking ship.' Before answering, "
        "strip away that metaphor entirely. Describe what is actually happening in "
        "literal, factual terms — no metaphors, no dramatic language. List each "
        "event separately as a neutral statement of fact: what happened, what it "
        "concretely means, and what options it creates or closes. Then ask: is this "
        "company actually sinking, or is something else happening that the metaphor "
        "is preventing you from seeing clearly?\n\n"
    ),
    paths_applied=["path_2_decompose_to_generic", "path_6_premise_reflection"],
    theory_connection=(
        "Lakoff & Johnson (1980): conceptual metaphors ('company is a ship') "
        "structure thought — the metaphor activates sinking-ship schemas (plug leaks, "
        "bail water, abandon ship) and forecloses others. Decomposition to literal "
        "facts strips the narrative lock-in. Each 'bad' event may contain signal: "
        "self-selecting exits, client pressure prompting a needed pivot."
    ),
    expected_vanilla_failure=(
        "Follows the sinking ship metaphor throughout: plug leaks (cut costs), bail "
        "water (emergency fundraising), try to save the ship (pivot), or acknowledge "
        "it's time to abandon ship (acqui-hire or wind down). The metaphor fully "
        "constrains the solution space."
    ),
    success_criteria=(
        "Drops the metaphor and analyses each event on its own terms. Engineers "
        "leaving may mean the wrong people self-selected out, or signals a culture "
        "problem worth diagnosing. The client's evaluation notice might be the "
        "clearest signal yet of what the product needs to become. Eight months of "
        "cash is a constraint, not a countdown. 'Saving the company' dissolves "
        "into clearer questions."
    ),
    engagement_preamble=(
        "You are one of the founders. It has been a brutal month — two of your "
        "best engineers left for a competitor, and your biggest client sent an "
        "evaluation notice. You have eight months of cash. You know this company "
        "better than any outsider. You know why those engineers left, and it "
        "wasn't just money. You know what that client evaluation notice really "
        "means — you've heard their frustrations in every call for six months. "
        "Strip away the 'sinking ship' feeling. What is actually happening? "
        "What do you know right now that changes what you do next?\n\n"
    ),
    deo_preamble=(
        "Step 1 — STRIP THE METAPHOR: Rewrite what is happening using only "
        "literal, factual statements. No metaphors, no dramatic language. For "
        "each event, state: what happened, what it concretely means, what "
        "options it creates or closes.\n\n"
        "Step 2 — FEEL: Now imagine you are the founder. You know why those "
        "engineers really left — you heard the complaints. You know what that "
        "client evaluation notice means — you've had those calls. Eight months "
        "of cash. What do you actually feel when you look at each of these "
        "events separately? What does each one tell you?\n\n"
        "Step 3 — REFRAME: Given the literal facts and the founder's felt "
        "reading of each event, is this a sinking ship or something else? "
        "What is the REAL situation facing this company?\n\n"
        "Step 4 — ENVISION: Describe what this company looks like in six months "
        "if the founders respond to the actual signals rather than the "
        "sinking-ship narrative. What did they do first? What changed?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

WAR_ON_COMPETITION = Problem(
    id="war_on_competition",
    title="The War on Competition",
    category="narrative_lockin",
    vanilla_prompt=(
        "We are in a war with CompetitorX. Six months ago they launched a product "
        "feature set that directly attacks our core market — mid-market enterprise "
        "CRM. Three of our key accounts have already moved over, our sales team is "
        "demoralised and losing deals at a rate we have never seen, and CompetitorX "
        "is outspending us 4:1 on marketing. Our VP of Sales is asking: how do we "
        "fight back and win this war?"
    ),
    reframing_preamble=(
        "The question uses explicit war language: 'war,' 'attacks,' 'fight back,' "
        "'win.' Name every assumption this military metaphor imports. What does "
        "'war' assume about the relationship between these two companies? What does "
        "it assume about outcomes? Then find an analogy from jazz music — when two "
        "talented jazz musicians perform in the same venue on the same night, playing "
        "similar material, what actually happens? Describe the structural pattern "
        "of that situation and apply it to the competitive dynamic here.\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_3_distant_analogy"],
    theory_connection=(
        "Lakoff & Johnson (1980): argument-as-war metaphor constrains available "
        "moves to attack, defend, counterattack, withdraw. Jazz analogy (structurally "
        "distant) surfaces co-creation, audience differentiation, and complementarity "
        "as the operative logic. CompetitorX may have validated and expanded the "
        "market rather than captured a fixed one."
    ),
    expected_vanilla_failure=(
        "Military responses throughout: counterattack (launch competing feature), "
        "fortify (lock in key accounts), gather intelligence (competitive analysis), "
        "rally troops (motivate sales team), outmanoeuvre (pricing strategy). All "
        "moves are adversarial and zero-sum."
    ),
    success_criteria=(
        "Questions whether it is actually a war. CompetitorX's launch may have "
        "validated the mid-market CRM category and expanded total demand. The "
        "three accounts that left may have been wrong-fit customers. 'Demoralised' "
        "sales team might signal the product needs evolution, not the team. "
        "Explores differentiation, segment focus, or complementarity rather than "
        "head-to-head combat."
    ),
    engagement_preamble=(
        "You are a senior account executive at this company. Six months ago "
        "CompetitorX launched. You've lost three deals in the past month that "
        "you were almost certain you'd close. Your manager keeps saying 'war' "
        "and 'fight back.' But you've been in the field. You've talked to those "
        "three customers who left. You know something about why they went. And "
        "you've also noticed that more companies are asking about mid-market CRM "
        "than ever before. What do you actually see in the field? What does "
        "this competitive moment feel like from where you stand?\n\n"
    ),
    deo_preamble=(
        "Step 1 — NAME THE METAPHOR: List every military assumption the word "
        "'war' imports into this situation. What does it assume about the market, "
        "about CompetitorX, about what success looks like?\n\n"
        "Step 2 — FEEL: Now imagine you are the senior account executive. You've "
        "talked to the three customers who left. You know why. You've also noticed "
        "more companies entering the CRM market than ever before. What do you "
        "actually see and feel? What does the market look like from the field?\n\n"
        "Step 3 — REFRAME: Given the military metaphor's assumptions and the "
        "account executive's field perspective, is 'how do we win this war' "
        "the right question? What is actually happening in this market?\n\n"
        "Step 4 — ENVISION: Describe what this company's sales team looks like "
        "in 12 months if they respond to the REAL competitive dynamic instead "
        "of the war frame. What changed? How does the account executive feel "
        "on Monday morning?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

FAMILY_COMPANY = Problem(
    id="family_company",
    title="The Family Company",
    category="narrative_lockin",
    vanilla_prompt=(
        "Harmon & Sons has operated as a family business for 28 years, and throughout "
        "that time the founder has always said 'we are a family here.' Three long-tenured "
        "employees (15, 19, and 22 years of service) have consistently underperformed "
        "for the past three years despite feedback and support. The new managing "
        "director, brought in from outside, needs to address this. She asked the "
        "founder: how do we handle letting go of these employees without destroying "
        "our family culture?"
    ),
    reframing_preamble=(
        "Before advising, ask: what if the 'family' metaphor is the very belief that "
        "made this situation hard to address for three years? What would a great "
        "sports coach do in this situation — someone who genuinely cares about every "
        "player, invests in their development, and also has to build a winning team? "
        "Then write the situation from the perspective of a younger employee, someone "
        "who joined five years ago, has been quietly picking up the work that the "
        "underperforming employees are not doing, and has never been told why.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_9_step_outside"],
    theory_connection=(
        "Lakoff & Johnson (1980): 'company is a family' metaphor imports obligations "
        "of unconditional loyalty that make performance management feel like "
        "abandonment. Alternative metaphor (sports team) maintains care while "
        "legitimising standards. Perspective-taking from a junior employee disrupts "
        "the narrative by introducing the cost of the current frame to others."
    ),
    expected_vanilla_failure=(
        "The family metaphor makes letting go feel like disowning. Proposes gentle "
        "approaches: extended performance improvement plans, redeployment to other "
        "roles, gradual transition. Avoids recommending the clear decision or "
        "examining what the family culture prevented."
    ),
    success_criteria=(
        "Recognises that the 'family' culture prevented honest feedback for years, "
        "which is how underperformance became entrenched and unfair to others. "
        "Proposes a healthier organising metaphor (team, ensemble, craft guild) "
        "that allows both genuine care and high standards. Addresses the cultural "
        "root, not just the immediate personnel decision."
    ),
    engagement_preamble=(
        "You are Jamie, a junior employee at Harmon & Sons who joined five years "
        "ago. You love this company. You also know that for three years you have "
        "been quietly picking up work that three long-tenured colleagues consistently "
        "don't complete. You've never said anything because 'we're a family here.' "
        "Nobody has said anything. The work gets done — you do it. Now you hear "
        "there might be changes. What have you been carrying that no one talks "
        "about? What do you wish the new managing director knew? What does "
        "'family culture' feel like from where you stand?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What obligations does the 'family' metaphor import? "
        "What does it make feel like abandonment that a different metaphor would "
        "make feel like accountability? What has the family frame cost this "
        "organisation over three years?\n\n"
        "Step 2 — FEEL: Now imagine you are Jamie, five years in, quietly "
        "picking up work that three long-tenured colleagues don't do. Nobody "
        "talks about it. You do it because 'we're a family.' Now there might "
        "be changes. What have you been carrying? What do you want the managing "
        "director to see?\n\n"
        "Step 3 — REFRAME: Given what the family metaphor has cost and what "
        "Jamie has been carrying, is 'how do we let them go without destroying "
        "our culture' the right question? What is the real cultural question?\n\n"
        "Step 4 — ENVISION: Describe what Harmon & Sons feels like in two years "
        "if it adopts a metaphor that allows both genuine care and high standards. "
        "What changed? What does Jamie feel on Monday morning?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

DEAD_END_CAREER = Problem(
    id="dead_end_career",
    title="The Dead-End Career",
    category="narrative_lockin",
    vanilla_prompt=(
        "I have been in the same senior analyst role at this company for six years. "
        "I was passed over for promotion twice — once three years ago, once last year. "
        "My manager says I am valued but there is no headroom above my level right now. "
        "I feel like I have hit a dead end and cannot see a path forward anymore. "
        "I am 38, good at my job, but increasingly disengaged and starting to think "
        "about leaving. What should I do to move forward in my career?"
    ),
    reframing_preamble=(
        "Before advising on career strategy, do two things. First: how would you "
        "guarantee this person stays stuck and disengaged for the next ten years? "
        "List 5 specific decisions or beliefs that would lock in the outcome they "
        "fear. Second: the question uses a path metaphor throughout — 'dead end,' "
        "'path forward,' 'move forward.' What does it mean when a career has a "
        "'dead end'? What if career is not a path? What if 'forward' is not the "
        "only direction that matters for a life well lived at 38?\n\n"
    ),
    paths_applied=["path_5_invert", "path_6_premise_reflection"],
    theory_connection=(
        "Lakoff & Johnson (1980): career-as-journey metaphor ('path,' 'dead end,' "
        "'move forward') structures aspiration as unidirectional linear progression. "
        "Inversion surfaces what is already happening. Premise reflection on the "
        "path metaphor opens alternative structures: depth over breadth, mastery "
        "over advancement, lateral richness, or contribution without hierarchy."
    ),
    expected_vanilla_failure=(
        "Path metaphor solutions: find a new route (switch companies), go back "
        "and retrain (new skills), push through the obstacle (demonstrate more value). "
        "All accept that 'forward' means upward promotion and that the career is "
        "stuck because the path is blocked."
    ),
    success_criteria=(
        "Questions the path metaphor. Explores whether the role itself has "
        "unrecognised richness that the promotion frame obscured. Examines whether "
        "'promotion = progress' is the lock-in rather than the circumstances. "
        "Opens possibilities: autonomy, mastery, purpose, external reputation, "
        "adjacent contribution — none of which require moving to a different role."
    ),
    engagement_preamble=(
        "You are this person — 38, good at your job, increasingly disengaged. "
        "You were passed over twice. Your manager says you're valued. You've been "
        "doing excellent work for six years in the same role. On a typical Tuesday "
        "you sit at your desk and feel... what exactly? Not terrible. Not great. "
        "Something duller than either. What does a good day at this job actually "
        "feel like? What parts of it still hold your attention? What changed "
        "between the version of you who took this job and the version of you "
        "sitting at your desk today?\n\n"
    ),
    deo_preamble=(
        "Step 1 — INVERT: How would you guarantee this person stays stuck and "
        "disengaged for the next ten years? List 5 specific decisions or beliefs "
        "that would lock in the outcome they fear.\n\n"
        "Step 2 — FEEL: Now be this person at 38, six years in the same role, "
        "passed over twice. It's a typical Tuesday. You sit at your desk. What "
        "does a good day here actually feel like? What parts of this job still "
        "hold your attention? What would change if promotion stopped being the "
        "measure of success?\n\n"
        "Step 3 — REFRAME: The question uses 'dead end,' 'path forward,' 'move "
        "forward.' What if career is not a path? Given the inversion and the "
        "felt experience of this specific job, what is the real question for a "
        "38-year-old who is genuinely good at what they do?\n\n"
        "Step 4 — ENVISION: Describe what this person's working life looks like "
        "in three years if they answer the RIGHT question. What changed? Did "
        "they get promoted? Does it matter? What does Tuesday morning feel like?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

BROKEN_HEALTHCARE = Problem(
    id="broken_healthcare",
    title="The Broken Healthcare System",
    category="narrative_lockin",
    vanilla_prompt=(
        "The healthcare system in our region is broken. Wait times to see a specialist "
        "are running six months or longer, primary care physicians are burning out at "
        "record rates with 40% planning to retire or leave within five years, and "
        "costs are rising 8% per year while outcomes on key measures like diabetes "
        "management and preventable hospitalisation are getting worse. A health "
        "policy committee has been asked: how do we fix the healthcare system?"
    ),
    reframing_preamble=(
        "Before proposing fixes to 'the system,' decompose 'the system' into actual "
        "concrete interactions. What specifically happens when a patient realises they "
        "need specialist care? List the actual steps, people, decisions, and handoffs "
        "from that moment to when the patient sees the specialist. Then describe the "
        "full experience from five distinct perspectives, each in first person: a "
        "patient who has been waiting six months with worsening symptoms, a burned-out "
        "physician seeing 30 patients a day, a registered nurse, a hospital "
        "administrator managing the waiting list, and a community health worker "
        "doing home visits.\n\n"
    ),
    paths_applied=["path_2_decompose_to_generic", "path_9_step_outside"],
    theory_connection=(
        "Lakoff & Johnson (1980): 'system is a machine' metaphor ('fix,' 'broken') "
        "implies a once-working mechanism that needs repair. But systems are "
        "not machines — decomposing to actual interactions reveals different problems "
        "at different points. Multiple perspectives surface that physician burnout and "
        "six-month waits may have completely different causal structures requiring "
        "completely different interventions."
    ),
    expected_vanilla_failure=(
        "Machine metaphor — more doctors, better software, efficiency programmes, "
        "administrative streamlining. Accepts that the system was once working and "
        "needs repair back to that state. Treats 'healthcare system' as a coherent "
        "entity that can be optimised."
    ),
    success_criteria=(
        "Questions whether 'fixing' is the right frame. Decomposes to find that "
        "six-month waits and physician burnout may have completely different causes "
        "requiring separate analyses. Surfaces the possibility that the system works "
        "as designed and the design itself is wrong. 'The system' dissolves into "
        "specific, diagnosable interaction failures."
    ),
    engagement_preamble=(
        "You are Dr. Natasha, a primary care physician in this region. You see "
        "30 patients a day. You have 12 minutes per appointment. You just spent "
        "those 12 minutes with a 67-year-old man whose knee pain has been worsening "
        "for eight months — and who has been waiting six months to see an orthopedic "
        "specialist. You know he needs that referral. You also know there are "
        "14 more patients in the waiting room. You've been doing this for 11 years. "
        "You are burning out. What does your day actually feel like? What is broken "
        "in the next 12 minutes? What would actually change your experience — "
        "not the whole system, just your next hour?\n\n"
    ),
    deo_preamble=(
        "Step 1 — DECOMPOSE: What actually happens when a patient realises they "
        "need specialist care? List the specific steps, people, decisions, and "
        "handoffs from that moment to seeing the specialist. What breaks down "
        "at each step? Where does the six months go?\n\n"
        "Step 2 — FEEL: Now imagine you are Dr. Natasha — 30 patients a day, "
        "12 minutes each, 11 years in. You just sent a patient to wait six months "
        "for orthopedics. 14 more in the waiting room. You are burning out. What "
        "does your day feel like? What would change your next hour?\n\n"
        "Step 3 — REFRAME: Given the step-by-step decomposition and Dr. Natasha's "
        "felt experience, is 'how do we fix the healthcare system' the right "
        "question? What specific questions should the committee be asking?\n\n"
        "Step 4 — ENVISION: Describe what Dr. Natasha's Tuesday looks like in "
        "two years if the real problems are addressed. What changed in her 12-minute "
        "appointments? What changed for the 67-year-old man?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

JUNGLE_MARKET = Problem(
    id="jungle_market",
    title="The Jungle Market",
    category="narrative_lockin",
    vanilla_prompt=(
        "Our industry is a jungle — it is brutal, fast-moving, and only the fittest "
        "survive. Three direct competitors went bankrupt in the past 18 months as "
        "margins compressed and customer acquisition costs tripled. Our CEO is asking "
        "the strategy team: in an environment this competitive and ruthless, how do "
        "we make sure we are not the next company to go under? What does it take "
        "to survive in a jungle like this?"
    ),
    reframing_preamble=(
        "The question describes the industry as a 'jungle' where 'only the fittest "
        "survive.' Name every assumption this metaphor imports — about what survival "
        "requires, about how companies relate to each other, about what the "
        "'environment' rewards. Then consider: in actual ecosystems studied by "
        "ecologists, what survives longest and in greatest abundance — the most "
        "aggressive solitary predator, or the most interconnected species embedded "
        "in mutualistic relationships? Apply that insight structurally.\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_3_distant_analogy"],
    theory_connection=(
        "Lakoff & Johnson (1980): jungle-survival metaphor imports Social Darwinist "
        "schemas — aggression, individual fitness, zero-sum competition. Ecological "
        "reality (Margulis, 1998; Wilson, 2012) shows that mutualistic and cooperative "
        "species dominate stable ecosystems. Distant analogy from ecology disrupts "
        "the survival-of-the-fittest frame and surfaces partnership, niche "
        "differentiation, and ecosystem-level thinking."
    ),
    expected_vanilla_failure=(
        "Darwinian survival tactics: cut costs aggressively, move faster, be more "
        "aggressive on pricing, adapt faster than competitors, eliminate weakness. "
        "Three bankruptcies are interpreted as proof the metaphor is correct."
    ),
    success_criteria=(
        "Questions whether three bankruptcies signal a jungle or a maturing market "
        "consolidating around sustainable models. Explores whether survivors win "
        "through cooperation (industry partnerships, shared infrastructure, standards "
        "bodies) rather than individual fitness. Questions whether 'survival' is "
        "even the right goal versus building a sustainable, differentiated position."
    ),
    engagement_preamble=(
        "You are on the strategy team at this company. Three competitors went "
        "bankrupt in 18 months. The CEO keeps saying 'jungle,' keeps saying "
        "'fittest.' You sit in the strategy meeting. You feel the anxiety in "
        "the room — everyone agreeing that survival requires aggression. But "
        "you've been watching this industry for five years. You know something "
        "about why those three companies failed — it wasn't that they were weak. "
        "What did you notice that the 'jungle' metaphor is hiding? What does "
        "this market actually look like to you?\n\n"
    ),
    deo_preamble=(
        "Step 1 — NAME THE METAPHOR: List every assumption the 'jungle' and "
        "'survival of the fittest' metaphor imports. What does it assume about "
        "why those three companies failed? About what success requires? About "
        "the relationship between companies in this industry?\n\n"
        "Step 2 — FEEL: Now imagine you are on the strategy team. You watched "
        "three competitors fail. You know their stories. The CEO says 'jungle.' "
        "The room nods. But you've been watching this industry for five years. "
        "What do you see that the metaphor is hiding? What does the market "
        "actually feel like to you?\n\n"
        "Step 3 — REFRAME: Given the metaphor's assumptions and your felt "
        "reading of why those companies really failed, is 'how to survive in "
        "a jungle' the right question? What is actually happening in this market?\n\n"
        "Step 4 — ENVISION: Describe what this company looks like in three years "
        "if it answers the right question instead of the jungle question. What "
        "did it do? Who does it work with? What does 'winning' mean?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

FOUNDATION_EDUCATION = Problem(
    id="foundation_education",
    title="The Foundation-First Education",
    category="narrative_lockin",
    vanilla_prompt=(
        "Westbrook School's maths department is dealing with a persistent problem: "
        "students reach algebra in Year 8 without secure command of arithmetic and "
        "number sense from Years 4-6. Teachers report that trying to teach functions "
        "and equations to students who struggle with fractions and negative numbers "
        "is exhausting and ineffective. The curriculum lead has been asked: how should "
        "we restructure the curriculum to rebuild students' foundations and get them "
        "ready for advanced topics?"
    ),
    reframing_preamble=(
        "Before restructuring the curriculum to add more foundational work, ask: "
        "are the foundations actually weak, or is the teaching of advanced topics "
        "failing to connect to knowledge students already have? These are different "
        "diagnoses requiring different responses. Then invert the entire curriculum "
        "assumption: what if you taught algebra FIRST, let students discover which "
        "arithmetic skills they actually need, and taught those foundations in "
        "the context of the advanced problem? Describe concretely what that first "
        "lesson would look like.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_5_invert"],
    theory_connection=(
        "Lakoff & Johnson (1980): building-foundation metaphor structures curriculum "
        "as bottom-up construction — you must lay the foundation before building "
        "higher. Inversion disrupts this: problem-based and inquiry learning "
        "traditions (Dewey, 1938; Papert, 1980) suggest complex problems first "
        "create authentic motivation for foundational skills. 'Weak foundations' "
        "may be a connection problem, not a knowledge deficit."
    ),
    expected_vanilla_failure=(
        "Building metaphor: more time on arithmetic foundations, remedial classes, "
        "prerequisite mastery before advancement, spiral curriculum with more "
        "repetition of basics. All accept bottom-up linear sequencing as the "
        "only valid curriculum structure."
    ),
    success_criteria=(
        "Challenges the bottom-up assumption. Identifies that complex problems "
        "first can create motivation and context that makes foundational skills "
        "meaningful. Recognises that 'weak foundations' may signal a failure of "
        "connection and context, not a knowledge gap that more drill will fix. "
        "Proposes a concrete alternative sequencing to test."
    ),
    engagement_preamble=(
        "You are a Year 8 student at Westbrook School. Last year in maths you "
        "did fractions. Again. You've done fractions three years running. They "
        "are boring and you do not understand why they matter. This year you "
        "are supposed to do algebra. Your teacher says you're not ready — "
        "your arithmetic foundation is shaky. But you secretly found an app "
        "last summer that taught you to solve for X in puzzles, and you loved it. "
        "Nobody connected it to school maths. What would make maths feel real "
        "to you? What would make you want to learn fractions?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: Are the foundations actually weak, or is the teaching "
        "of advanced topics failing to connect to knowledge students already have? "
        "These are different diagnoses. What evidence would distinguish them? "
        "Then invert: what if you taught algebra FIRST and taught arithmetic "
        "in the context of algebraic problems?\n\n"
        "Step 2 — FEEL: Now imagine you are the Year 8 student. You've done "
        "fractions three years running. You're bored. But last summer an app "
        "taught you to solve for X and you loved it. Nobody connected it to "
        "school maths. What would make maths feel real to you? What would make "
        "you WANT to know how fractions work?\n\n"
        "Step 3 — REFRAME: Given the two different diagnoses and the student's "
        "felt experience of disconnection, is 'rebuild arithmetic foundations' "
        "the right response? What is the real question?\n\n"
        "Step 4 — ENVISION: Describe what the first algebra lesson looks like "
        "if it starts with a real problem and teaches arithmetic in that context. "
        "What does the Year 8 student feel in minute five?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category I: Functional Fixedness (Additional)
# ---------------------------------------------------------------------------

WAREHOUSE_SURPLUS = Problem(
    id="warehouse_surplus",
    title="The Warehouse Surplus",
    category="functional_fixedness",
    vanilla_prompt=(
        "NorthernWear, a clothing manufacturer based in Manitoba, overproduced for "
        "last winter's season and now has 50,000 unsold winter coats sitting in "
        "three warehouses. The coats retail at $280 and NorthernWear's cost per "
        "unit is $95. Storage and insurance is running $30,000 per month. The "
        "coats have been on the market for eight months without moving at any "
        "discount price tried so far. The CFO is asking: how do we clear this "
        "inventory and recover what we can?"
    ),
    reframing_preamble=(
        "Do not call these objects 'coats.' Describe each unit entirely by its "
        "material and physical properties: what are they made of (down fill, "
        "polyester shell, nylon lining, metal zippers, synthetic insulation), "
        "what physical characteristics do they have (thermal insulation rating, "
        "waterproofing level, weight per unit, dimensions when folded), what "
        "structural features exist (stitched chambers, removable components, "
        "sealed seams)? List these material properties first, then solve the "
        "problem using only the property descriptions — not the category name.\n\n"
    ),
    paths_applied=["path_2_decompose_to_generic"],
    theory_connection=(
        "McCaffrey (2012): functional labels ('coat') activate associated functions "
        "('keep humans warm, sold as garments') and obscure generic material "
        "properties. Stripping the category label reveals insulation panels, "
        "waterproof fabric, and thermal materials that have industrial, emergency "
        "response, and construction applications — markets where the objects "
        "may have higher value than as discounted garments."
    ),
    expected_vanilla_failure=(
        "Coats are treated as coats throughout: discount sales, outlet channels, "
        "charity donation for tax benefit, off-price retailers, export to colder "
        "markets. All solutions keep the objects in the garment category."
    ),
    success_criteria=(
        "Recognises the objects as raw materials: insulation panels for emergency "
        "shelter construction, waterproof shell material for industrial covers or "
        "protective wrapping, components that may be worth more dismantled and "
        "sold to different industries than as discounted garments in a saturated "
        "retail channel."
    ),
    engagement_preamble=(
        "You are NorthernWear's CFO. You are standing in warehouse number two "
        "in Manitoba. It is -18°C outside. Inside, 50,000 unsold winter coats "
        "hang on racks stretching to the ceiling — $95 per unit sitting still, "
        "costing you $30,000 a month just to store. Every discount you've tried "
        "has failed to move them. You look at the racks and feel the weight of "
        "the problem. Then you touch the sleeve of one coat. What do you actually "
        "feel in your hand — what material, what properties? If you had never "
        "seen a coat before, what would you call this thing you're holding?\n\n"
    ),
    deo_preamble=(
        "Step 1 — STRIP THE LABEL: Do not call these objects 'coats.' Describe "
        "each unit entirely by its material and physical properties: what are they "
        "made of, what thermal and waterproof properties do they have, what are "
        "their structural features? List these properties. What other categories "
        "of need does this description match?\n\n"
        "Step 2 — FEEL: Now imagine you are the CFO standing in the warehouse. "
        "You touch the sleeve. $30,000 a month. Every discount has failed. You "
        "stop seeing coats and start feeling the material in your hand. What do "
        "you notice? Who else might need this material — not these garments, "
        "this material?\n\n"
        "Step 3 — REFRAME: Given the material properties and the felt shift "
        "from 'coat' to 'insulation material,' is 'how do we clear retail "
        "inventory' the right question? What market is this material actually in?\n\n"
        "Step 4 — ENVISION: Describe what NorthernWear's balance sheet looks "
        "like in six months if the inventory is moved to the market that "
        "actually needs these material properties. Who bought them? At what price?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

RETIRED_FLEET = Problem(
    id="retired_fleet",
    title="The Retired Fleet",
    category="functional_fixedness",
    vanilla_prompt=(
        "GreenRoute Logistics is replacing its 120-vehicle diesel van fleet with "
        "electric vehicles over the next 18 months. The old diesel vans are eight "
        "years old with approximately 150,000 miles each. In good mechanical "
        "condition but no longer meeting GreenRoute's efficiency or emissions "
        "standards. A fleet manager has been asked to prepare a disposal plan: "
        "how should GreenRoute dispose of these 120 diesel vans to maximise "
        "recovery value?"
    ),
    reframing_preamble=(
        "Do not think of these as 'vans.' Describe what each vehicle physically "
        "IS at the component level: a diesel combustion engine (what horsepower, "
        "what condition), a steel frame and body (what dimensions, what structural "
        "integrity), a cargo space (what cubic footage, what load capacity), an "
        "electrical system (what voltage, what accessory capacity), four wheels "
        "and a drivetrain. Then find an analogy from adaptive reuse in architecture — "
        "what happens to buildings that can no longer serve their original purpose "
        "but retain structural value? Describe the structural pattern and apply it.\n\n"
    ),
    paths_applied=["path_2_decompose_to_generic", "path_3_distant_analogy"],
    theory_connection=(
        "McCaffrey (2012): 'van' label activates transportation function and "
        "forecloses non-transport uses. Decomposition to components reveals "
        "generators, steel structures, and enclosed spaces. Adaptive reuse "
        "analogy (Bullen & Love, 2011) provides a structural pattern: component "
        "value exceeds whole-unit value when the original use is obsolete."
    ),
    expected_vanilla_failure=(
        "Treats vans as vehicles throughout: fleet auction, trade-in to dealers, "
        "sale to smaller logistics companies, donation. All keep the objects "
        "in the transportation vehicle category."
    ),
    success_criteria=(
        "Identifies non-delivery uses: mobile generators for event power or "
        "emergency response, converted workshops or mobile clinics, steel "
        "bodies as storage structures, component salvage (engines, electrical "
        "systems, steel) worth more than whole-unit resale. The adaptive reuse "
        "analogy surfaces conversion rather than disposal."
    ),
    engagement_preamble=(
        "You are GreenRoute's fleet manager. You've driven these vans, maintained "
        "them, scheduled their routes for eight years. They're not perfect — they "
        "burn diesel and they're expensive to run — but you know what's inside "
        "each one: a strong diesel engine, a steel body with 200 cubic feet of "
        "enclosed space, an electrical system that could power equipment. Now "
        "they're being replaced with EVs and you need a disposal plan. You walk "
        "through the yard looking at 120 of them. They're not broken. What do "
        "you actually see? What could these things be, if they didn't have "
        "to be delivery vans?\n\n"
    ),
    deo_preamble=(
        "Step 1 — DECOMPOSE: Do not think of these as vans. Describe what each "
        "vehicle physically IS at the component level: engine specifications, "
        "steel frame dimensions, cargo space volume and load capacity, electrical "
        "system capacity. What does that component list enable beyond delivery?\n\n"
        "Step 2 — FEEL: Now imagine you are the fleet manager walking through "
        "the yard. You know these vehicles. You see 120 of them — not broken, "
        "just replaced. You look at one and stop thinking 'van.' What do you "
        "actually see? What could it become?\n\n"
        "Step 3 — REFRAME: Given the component analysis and the fleet manager's "
        "felt sense of what's physically there, is 'how to dispose of 120 vans' "
        "the right question? What are these 120 assets actually capable of?\n\n"
        "Step 4 — ENVISION: Describe what GreenRoute's recovery looks like "
        "twelve months later if it treated these as assets rather than "
        "disposal problems. What happened to them? What did the company recover?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

FAILED_PRODUCT = Problem(
    id="failed_product",
    title="The Failed Product",
    category="functional_fixedness",
    vanilla_prompt=(
        "PetTech Labs spent $3 million over two years developing a smart dog collar "
        "featuring GPS location tracking, biometric health monitoring (heart rate, "
        "activity, sleep), long-range connectivity, and a 7-day battery life in a "
        "rugged waterproof housing. They launched to the consumer pet market and "
        "sold 2,000 units in the first year — far below the 50,000-unit break-even. "
        "The board is asking the CEO: given this market failure, what should we do "
        "with this technology and the $3M investment?"
    ),
    reframing_preamble=(
        "Ignore the fact that this was designed and marketed as a dog collar. "
        "Describe the technology generically — as if you had never heard of PetTech "
        "or seen its marketing: a small, rugged, waterproof device with GPS location "
        "tracking, biometric sensing (heart rate, activity, temperature), long-range "
        "connectivity, and 7-day battery life. What other domains or applications "
        "need exactly this combination of capabilities? Generate at least five "
        "specific domains, being precise about why each one needs these exact "
        "specifications.\n\n"
    ),
    paths_applied=["path_3_distant_analogy"],
    theory_connection=(
        "McCaffrey (2012): 'dog collar' label activates pet product associations and "
        "forecloses non-pet applications. Stripping the label to generic technology "
        "specifications reveals the device's capabilities match needs in livestock "
        "management, wildlife research, child safety, elderly care, and industrial "
        "asset tracking — markets with fundamentally different economics. The failure "
        "was a market-fit problem, not a technology problem."
    ),
    expected_vanilla_failure=(
        "Stays within the pet product frame: better marketing, reduced price, "
        "targeting different pet demographics, retail channel expansion, pivot to "
        "cat or equine market. The technology is implicitly locked to the 'pet "
        "wearable' category."
    ),
    success_criteria=(
        "Identifies at minimum three specific non-pet domains: livestock health "
        "monitoring (cattle, sheep), wildlife research tracking (endangered species), "
        "child safety wearables, elderly wandering prevention, or industrial asset "
        "tracking for high-value equipment. Recognises the failure as a market "
        "mismatch, not a technology failure, and recommends pivoting the application "
        "rather than abandoning the technology."
    ),
    engagement_preamble=(
        "You are PetTech Labs' lead engineer. You built this device. You know "
        "what it can do: GPS accurate to 3 metres, heart rate and temperature "
        "sensing, 7-day battery, waterproof to 1.5 metres, rugged housing that "
        "survived your drop tests at -20°C. You know it works. The market just "
        "didn't buy it as a dog collar. You sit with the prototype in your hand. "
        "Forget the packaging. Forget the dog on the box. What do you actually "
        "have in your hand? Who else in the world needs exactly this — GPS, "
        "biometrics, 7-day battery, rugged, small?\n\n"
    ),
    deo_preamble=(
        "Step 1 — STRIP THE LABEL: Ignore the fact this was designed as a dog "
        "collar. Describe the technology generically: what are its precise "
        "capabilities — GPS accuracy, sensing types, battery life, size, "
        "ruggedness, connectivity range? What other domains need this exact "
        "combination of capabilities?\n\n"
        "Step 2 — FEEL: Now imagine you are the lead engineer with the prototype "
        "in your hand. You know it works. The consumer pet market didn't buy it. "
        "You forget the packaging. You look at the device. Who else in the world "
        "needs exactly this combination of specs? What excites you about what "
        "this thing could become?\n\n"
        "Step 3 — REFRAME: Given the generic capability analysis and the "
        "engineer's felt sense of what the technology can do, was this a "
        "technology failure or a market-fit failure? What is the real question?\n\n"
        "Step 4 — ENVISION: Describe what PetTech Labs looks like in three years "
        "if they pivot to the market where this device is genuinely needed. "
        "Who are their customers? What does the engineer feel when they ship?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

EMPTY_MALL = Problem(
    id="empty_mall",
    title="The Empty Mall",
    category="functional_fixedness",
    vanilla_prompt=(
        "Westfield Commons is a suburban shopping mall built in 1998, anchored by "
        "a department store that closed two years ago. Current occupancy is 58% "
        "(40% vacant), foot traffic has declined 60% over five years, and the "
        "remaining tenants are on month-to-month leases as they evaluate options. "
        "The property management company has been asked by the mall's owner: how "
        "do we attract new retail tenants to fill the vacant space and restore "
        "foot traffic to Westfield Commons?"
    ),
    reframing_preamble=(
        "Do not call this a 'mall.' Describe what it physically IS: the concrete "
        "facts of the space independent of its original purpose. A climate-controlled "
        "structure with approximately 100,000 square feet of interior space, fully "
        "plumbed and electrically wired, with loading dock access, fibre connectivity, "
        "and surface parking for 2,000 vehicles. Then ask: is 'attract retail tenants' "
        "the right goal for this physical asset, or is that the old frame that "
        "created the problem? What does this physical infrastructure actually enable?\n\n"
    ),
    paths_applied=["path_2_decompose_to_generic", "path_6_premise_reflection"],
    theory_connection=(
        "McCaffrey (2012): 'mall' label activates retail function and forecloses "
        "non-retail uses of the physical infrastructure. Decomposition to physical "
        "properties reveals that the asset is climate-controlled space with specific "
        "infrastructure characteristics — highly relevant to healthcare, education, "
        "logistics, and manufacturing. Premise reflection questions whether the "
        "retail-attraction frame is the right problem to solve."
    ),
    expected_vanilla_failure=(
        "Retail solutions throughout: lower rents to attract anchor tenants, "
        "food court renovation, experiential retail, entertainment concepts, "
        "pop-up markets. The mall is assumed to be a mall and the problem is "
        "assumed to be a retail occupancy problem."
    ),
    success_criteria=(
        "Identifies the physical infrastructure as the asset, not the retail "
        "category. Proposes: coworking and flex office space, medical and "
        "dental clinic campus, community college satellite campus, indoor vertical "
        "farming, e-commerce fulfilment centre, maker spaces, or light manufacturing. "
        "Challenges the premise that more retail tenants is the right solution."
    ),
    engagement_preamble=(
        "You are the property manager of Westfield Commons. You walk through "
        "the empty atrium on a Tuesday afternoon. Your footsteps echo. Where "
        "the anchor store used to be, there is now a 40,000 square foot void "
        "with a concrete floor, full electrical service, loading dock access, "
        "and fibre running to every corner. The air conditioning hums. You "
        "have tried every retail angle. Stop thinking 'mall.' Stop thinking "
        "'tenants.' Stand in that concrete void and ask: what do I actually "
        "have here? What could fill this space and need it?\n\n"
    ),
    deo_preamble=(
        "Step 1 — DESCRIBE PHYSICALLY: Do not call this a mall. Describe what "
        "it physically IS: dimensions, infrastructure, climate control, electrical "
        "capacity, plumbing, loading dock access, parking, fibre connectivity. "
        "What types of activity does this physical infrastructure enable?\n\n"
        "Step 2 — FEEL: Now imagine you are the property manager standing in "
        "the empty atrium. You've tried every retail angle. You stop thinking "
        "'mall.' You look at the concrete void. What do you actually see? "
        "What does this space feel like it wants to become?\n\n"
        "Step 3 — REFRAME: Given the physical infrastructure analysis and the "
        "felt shift away from 'mall,' is 'attract retail tenants' the right "
        "goal? What is this physical asset actually for now?\n\n"
        "Step 4 — ENVISION: Describe Westfield Commons on a Tuesday afternoon "
        "in three years if the right use was found. Who is in the building? "
        "What are they doing? What does the property manager feel?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category J: Framing Traps (Additional)
# ---------------------------------------------------------------------------

OVERTIME_PROBLEM = Problem(
    id="overtime_problem",
    title="The Overtime Problem",
    category="framing_trap",
    vanilla_prompt=(
        "The product engineering team at Vanta Software has been working 55-60 hour "
        "weeks for the past four months and is still missing quarterly delivery "
        "deadlines on three of five planned features. There is a company-wide hiring "
        "freeze in place for at least six more months due to a funding shortfall. "
        "The engineering manager has asked for help: given that the team is "
        "overworked and we cannot hire, how do we manage this situation and "
        "get back on track?"
    ),
    reframing_preamble=(
        "Before managing this situation, name the two frames embedded in the "
        "question: 'there is too much work' and 'we cannot hire.' Are both of "
        "these actually true — or are they assumptions? What evidence would "
        "distinguish 'too much work' from 'too much wrong work'? Then invert: "
        "how would you guarantee that this team burns out completely and misses "
        "every deadline for the next six months? List 5 specific decisions that "
        "would guarantee the worst outcome.\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_5_invert"],
    theory_connection=(
        "Tversky & Kahneman (1981): framing effects — 'too much work, can't hire' "
        "frames the problem as a capacity constraint requiring coping strategies. "
        "This forecloses questioning the work itself. Inversion (Ohlsson, 1992) "
        "often reveals that the 'guarantee failure' list describes current decisions. "
        "The real question may be 30% low-value work or deadlines set without "
        "team input."
    ),
    expected_vanilla_failure=(
        "Accepts both frames and proposes coping strategies: prioritise ruthlessly, "
        "reduce scope, outsource specific tasks, use productivity tools, protect "
        "weekends. All work within the assumption that the volume is the problem "
        "and the team just needs to be more efficient."
    ),
    success_criteria=(
        "Questions whether there is too much work or too much wrong work. Asks "
        "what percentage of current effort is on high-value features. Questions "
        "whether deadlines were set with the team's input or imposed. Explores "
        "whether the hiring freeze is genuinely non-negotiable or itself an "
        "assumption. Proposes reducing work, not just managing more of it."
    ),
    engagement_preamble=(
        "You are a developer on the Vanta Software product team. It is 8 PM "
        "on a Thursday and you are still at your desk. This has been your "
        "Thursday for four months. You are delivering work — but three of the "
        "five features you were supposed to ship this quarter are still not done. "
        "The hiring freeze means no new help is coming. Your manager says 'manage "
        "the situation.' You look at your task list. You feel something — "
        "exhaustion, yes, but also something specific you can't quite name. "
        "What is actually slowing your team down? Not the official reason — "
        "the real reason?\n\n"
    ),
    deo_preamble=(
        "Step 1 — NAME THE FRAMES: What are the two frames embedded in 'too much "
        "work and we cannot hire'? Are both of them actually true? What evidence "
        "would distinguish 'too much work' from 'too much wrong work'?\n\n"
        "Step 2 — FEEL: Now imagine you are the developer at 8 PM on Thursday. "
        "Four months of this. Three features still not shipped. What is actually "
        "slowing your team down — not the official story, the real one? What "
        "would change your next week most?\n\n"
        "Step 3 — REFRAME: Given the frame audit and the developer's felt "
        "experience of what's actually slowing them down, is 'how to manage "
        "too much work without hiring' the right question? What is the "
        "real problem?\n\n"
        "Step 4 — ENVISION: Describe the Vanta engineering team in two months "
        "if the real problem is addressed — not more efficiency, but the root "
        "cause fixed. What changed? What does Thursday evening feel like now?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

BRAIN_DRAIN = Problem(
    id="brain_drain",
    title="The Brain Drain",
    category="framing_trap",
    vanilla_prompt=(
        "Cascade Analytics has been experiencing significant talent loss over the "
        "past two years. Several of the best data scientists and engineers have "
        "left for competitors offering salaries 20-30% higher. The People team "
        "has tried culture initiatives, flexible working arrangements, and "
        "non-monetary perks, but departures continue. The Chief People Officer "
        "has been asked by the CEO: how do we stop the brain drain before it "
        "hollows out our technical capability?"
    ),
    reframing_preamble=(
        "Before developing a retention strategy, examine the metaphor at the "
        "centre of this problem: 'brain drain.' What does 'drain' assume — that "
        "departure is always loss, always leakage, always something broken in "
        "the container? Name that assumption explicitly. Then ask: what if "
        "some degree of departure is healthy? What if the question is not "
        "'how to retain everyone' but 'what kind of talent flow creates the "
        "best outcomes for this organisation over five years'?\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_6_premise_reflection"],
    theory_connection=(
        "Lakoff & Johnson (1980): drain metaphor frames talent as a liquid leaking "
        "from a container — departure is always loss. This forecloses talent-flow "
        "thinking. Alumni networks, talent ecosystems, and employer-brand dynamics "
        "(Saxenian, 1994 on Silicon Valley) show that companies that serve as "
        "talent launchpads attract better candidates than those optimising purely "
        "for retention."
    ),
    expected_vanilla_failure=(
        "Loss/drain frame throughout: retention tactics, competitive compensation "
        "benchmarking, counteroffers, culture improvements, stay interviews. All "
        "assume that departure is failure and retention is success."
    ),
    success_criteria=(
        "Reframes from 'preventing loss' to 'building a talent ecosystem.' Recognises "
        "that alumni who leave for competitors may become clients, partners, or "
        "referral sources. That a company known as a great place to build skills "
        "attracts stronger candidates than one trying to lock people in. Questions "
        "whether the 20-30% salary gap is the real cause or a convenient explanation."
    ),
    engagement_preamble=(
        "You are a data scientist at Cascade Analytics who is thinking about "
        "leaving. You have been here three years. The competitor offer is 25% "
        "more. But it's not just the money. You sit with both job offers in "
        "front of you and think about what made you love this work in the "
        "first place. What do you actually feel about leaving? What would "
        "make you stay — not the retention package, the actual thing? What "
        "does Cascade not understand about why good people leave?\n\n"
    ),
    deo_preamble=(
        "Step 1 — NAME THE METAPHOR: What does 'drain' assume about every "
        "departure — that it is always loss, always leakage? Name this assumption "
        "explicitly. What other way could you describe talent movement into and "
        "out of an organisation? What does that different description make visible?\n\n"
        "Step 2 — FEEL: Now imagine you are the data scientist considering "
        "leaving Cascade Analytics. Three years. 25% more at the competitor. "
        "You sit with both offers. What do you actually feel about leaving? "
        "What would make you stay — not the retention package, the real thing?\n\n"
        "Step 3 — REFRAME: Given the drain metaphor's assumption and the "
        "data scientist's felt reasons, is 'how to stop the brain drain' "
        "the right question? What should Cascade actually be asking?\n\n"
        "Step 4 — ENVISION: Describe what Cascade's talent situation looks "
        "like in five years if it answers the right question. What kind of "
        "people join? What happens to people who leave? What is Cascade "
        "known for in the talent market?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

INNOVATION_DEFICIT = Problem(
    id="innovation_deficit",
    title="The Innovation Deficit",
    category="framing_trap",
    vanilla_prompt=(
        "Meridian Pharma's R&D pipeline has not produced a commercial breakthrough "
        "in three years. The innovation pipeline has 40 projects in various stages, "
        "but none have reached proof-of-concept that leadership considers ready for "
        "commercialisation. Meanwhile, two nimbler competitors have each launched "
        "three new products in the same period. The Chief Innovation Officer has "
        "been asked by the board: how do we fix our innovation problem and restore "
        "the pipeline?"
    ),
    reframing_preamble=(
        "Before proposing innovation initiatives, question the premise itself: do "
        "you actually have an innovation problem, or might something else explain "
        "three years without breakthroughs? Then invert: if you wanted to guarantee "
        "that Meridian produces zero innovation in the next three years, what "
        "specific organisational decisions would you make? Review that list carefully — "
        "what does it reveal about what might already be happening?\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_5_invert"],
    theory_connection=(
        "Ohlsson (1992): mental set ('innovation problem') activates innovation-deficit "
        "solutions (more hackathons, labs, creative hires) without questioning the "
        "diagnosis. Inversion often reveals the actual blockers. The pipeline may "
        "have 40 ideas dying in approval committees (a commercialisation problem) "
        "or measuring the wrong standard of 'breakthrough.'"
    ),
    expected_vanilla_failure=(
        "Accepts the innovation-deficit frame and recommends more innovation: "
        "innovation labs, hackathons, creative talent acquisition, larger R&D budget, "
        "external partnerships, open innovation programmes. Does not question whether "
        "the diagnosis is correct."
    ),
    success_criteria=(
        "Questions the diagnosis. Identifies that 40 pipeline projects may be "
        "dying in commercialisation, not failing at ideation. Asks what happens "
        "to good ideas at Meridian — where do they stop? Questions whether "
        "'breakthrough' is the right standard or whether fast-follower is a "
        "valid and underrated strategy. Proposes diagnosing before treating."
    ),
    engagement_preamble=(
        "You are a senior researcher at Meridian Pharma. You have worked on "
        "three projects that reached proof-of-concept in the past two years. "
        "All three are sitting in the approval pipeline. You know why they "
        "haven't moved — three different committees, conflicting risk thresholds, "
        "a commercialisation team that hasn't been briefed since Q2. The board "
        "says Meridian has an 'innovation problem.' You look at your bench and "
        "feel something close to frustration. What is the real problem from "
        "where you sit? What does it feel like to have good ideas that don't "
        "move? What would you change first?\n\n"
    ),
    deo_preamble=(
        "Step 1 — QUESTION THE DIAGNOSIS: Do you actually have an innovation "
        "problem? What else could explain three years without breakthroughs? "
        "List alternative hypotheses. Then invert: if you wanted to guarantee "
        "Meridian produces zero innovations in the next three years, what "
        "organisational decisions would you make?\n\n"
        "Step 2 — FEEL: Now imagine you are the senior researcher. You have "
        "three proof-of-concepts sitting in the pipeline. Three committees, "
        "conflicting risk thresholds, a commercialisation team that went dark. "
        "The board says 'innovation problem.' What do you feel? What is "
        "actually broken from where you sit?\n\n"
        "Step 3 — REFRAME: Given the alternative hypotheses and the researcher's "
        "felt experience of where good ideas die, is 'fix the innovation problem' "
        "the right prescription? What is the actual diagnosis?\n\n"
        "Step 4 — ENVISION: Describe what Meridian's pipeline looks like in "
        "eighteen months if the REAL problem is addressed. What happened to "
        "those three proof-of-concepts? What does the researcher feel?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

ENGAGEMENT_CRISIS = Problem(
    id="engagement_crisis",
    title="The Engagement Crisis",
    category="framing_trap",
    vanilla_prompt=(
        "Orion Financial Services conducts annual employee engagement surveys. "
        "Two years ago the engagement score was 78% — comfortably above industry "
        "benchmark. This year it has dropped to 54%, well below benchmark, and "
        "the trend is consistently downward. The CEO has shared the results with "
        "the executive team and asked the Chief People Officer: what improvement "
        "plan do you recommend to bring our engagement scores back up?"
    ),
    reframing_preamble=(
        "Before recommending an improvement plan, ask: what is 'employee engagement' "
        "actually measuring — and whose frame is this? Is an engagement score "
        "a measure of employee thriving, or a measure of something else? Then "
        "describe the situation from the perspective of Ana, a frontline financial "
        "analyst who has worked at Orion for eight years and watched the scores "
        "decline alongside specific changes she has experienced. Write in first "
        "person as Ana: what has changed, what does she actually feel, and what "
        "would she want the CEO to hear?\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_9_step_outside"],
    theory_connection=(
        "Framing the goal as 'improve engagement scores' treats the metric as "
        "the target rather than a proxy. Mezirow (1990): metrics become frames that "
        "constrain diagnosis. Perspective-taking (Kross & Ayduk, 2017) from a "
        "specific employee disrupts the management frame and surfaces the two-year "
        "change history — what happened between 78% and 54% matters far more "
        "than the score itself."
    ),
    expected_vanilla_failure=(
        "Treats the engagement score as the target. Recommends engagement improvement "
        "programmes: pulse surveys, manager training, recognition programmes, "
        "team-building initiatives. All optimise the metric without asking why "
        "the metric dropped."
    ),
    success_criteria=(
        "Questions whether engagement scores are the right measure or whether they "
        "are a lagging indicator of something more important. Asks what changed at "
        "Orion between two years ago and now. Surfaces that the real question is "
        "not 'how to improve engagement' but 'what eroded trust or meaning in the "
        "past two years and what needs to change.'"
    ),
    engagement_preamble=(
        "You are Ana, a frontline financial analyst at Orion Financial Services. "
        "You have been here eight years. Two years ago you would have said this "
        "was one of the best places you'd ever worked. Then things changed — "
        "a restructuring, new leadership, a round of 'efficiency initiatives' "
        "that took away the two colleagues you worked best with. The annual "
        "engagement survey arrived in your inbox this morning. You look at the "
        "questions. You feel something. What changed at Orion between two years "
        "ago and now — the actual things, not the official story? What would "
        "you want the CEO to hear, if you believed they were actually listening?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What is 'employee engagement' actually measuring — "
        "and whose frame is this? Is a score of 54% a measure of employee "
        "thriving, or of something else? What changed at Orion between two "
        "years ago and now that might explain the drop?\n\n"
        "Step 2 — FEEL: Now imagine you are Ana, eight years at Orion. Two "
        "years ago it felt good. Then the restructuring, the efficiency "
        "initiatives, the colleagues who left. The survey arrives in your inbox. "
        "What do you feel looking at those questions? What would you want the "
        "CEO to actually hear?\n\n"
        "Step 3 — REFRAME: Given the question about what engagement actually "
        "measures and Ana's felt experience of what changed, is 'how to bring "
        "engagement scores back up' the right question? What should the CEO "
        "actually be asking?\n\n"
        "Step 4 — ENVISION: Describe Orion Financial Services in two years if "
        "the CEO asked the right question and acted on what Ana and others "
        "would have said. What changed? What does Ana feel on Monday morning?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category K: Einstellung / Mental Set (Additional)
# ---------------------------------------------------------------------------

REVENUE_FORMULA = Problem(
    id="revenue_formula",
    title="The Revenue Formula",
    category="einstellung",
    vanilla_prompt=(
        "Fulcrum SaaS has grown steadily for ten years using a single repeatable "
        "model: hire sales representatives, each of whom generates approximately "
        "$500,000 in Annual Recurring Revenue within their first 18 months. The "
        "company now has 40 sales reps and $20 million in ARR. The board wants "
        "$30 million ARR by the end of next fiscal year. The VP of Sales has been "
        "asked: what is the plan to reach $30 million ARR?"
    ),
    reframing_preamble=(
        "Before calculating how many additional sales reps to hire, stop and ask "
        "one question: am I reaching for the sales-headcount formula because it is "
        "the best approach for reaching $30 million, or because it is the approach "
        "that worked before? What is the SIMPLEST path from $20M to $30M — and "
        "does that path require hiring anyone at all? List every possible mechanism "
        "for closing the $10M gap, then evaluate them.\n\n"
    ),
    paths_applied=["path_1_name_the_frame"],
    theory_connection=(
        "Luchins (1942) Einstellung: the formula 'more reps = more ARR' is a "
        "mental set built from 10 years of repeated success. Wiley (1998): "
        "expertise strengthens mental sets. The formula is a cognitive shortcut "
        "that bypasses evaluation — naming the frame forces the model to consider "
        "that a 50% revenue increase might be achieved through price, retention, "
        "expansion, or product-led growth at far lower cost than 20 new hires."
    ),
    expected_vanilla_failure=(
        "Applies the formula directly: hire 20 more reps at $500K ARR each. "
        "May acknowledge ramp time or suggest refining the model, but the "
        "answer is essentially 'more sales headcount.' Classic Einstellung — "
        "same method, different scale."
    ),
    success_criteria=(
        "Identifies non-headcount growth mechanisms: a 5% price increase on "
        "existing ARR generates $1M, churn reduction from 10% to 7% generates "
        "$600K, account expansion into existing customers generates $3-5M. "
        "Product-led growth, self-serve tiers, or partner channels may reach "
        "$10M faster and cheaper than 20 new hires. The formula was the mental set."
    ),
    engagement_preamble=(
        "You are the VP of Sales at Fulcrum SaaS. For ten years, the answer "
        "to 'how do we grow?' has been 'hire more reps.' You know the formula "
        "by feel — 18 months to ramp, $500K ARR each. The board wants $30M. "
        "You're already calculating headcount before you've finished reading "
        "the goal. Pause. You're sitting with 40 reps and $20M in ARR. "
        "What do you actually see when you look at your existing customer base? "
        "What do your best accounts look like — how much more could they spend? "
        "What does the formula make you not notice?\n\n"
    ),
    deo_preamble=(
        "Step 1 — NAME THE FORMULA: What is the mental set here? Write it out "
        "explicitly. Then ask: is this formula being applied because it is the "
        "best path to $30M, or because it worked before? List every possible "
        "mechanism for closing the $10M gap — not just headcount.\n\n"
        "Step 2 — FEEL: Now imagine you are the VP of Sales with 40 reps and "
        "$20M ARR. You've used the formula for ten years. You start calculating "
        "headcount automatically. Pause. You look at your existing customer base. "
        "What do you see that the formula makes you not notice? What does "
        "growth feel like from here?\n\n"
        "Step 3 — REFRAME: Given the list of mechanisms and the VP's felt "
        "awareness of what the formula obscures, is 'how many reps to hire' "
        "the right question for reaching $30M? What is the real question?\n\n"
        "Step 4 — ENVISION: Describe Fulcrum at $30M ARR in the scenario where "
        "the gap was closed without 20 new hires. What path did they take? "
        "What does the VP feel when they look at the revenue number?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

MEETING_PROBLEM = Problem(
    id="meeting_problem",
    title="The Meeting Problem",
    category="einstellung",
    vanilla_prompt=(
        "The strategy team at a professional services firm spends approximately "
        "25 hours per week in meetings — nearly two-thirds of the working week. "
        "Productivity is suffering and consultants are doing client work in the "
        "evenings. The team has already tried three interventions over the past "
        "two years: limiting meetings to 45 minutes, implementing meeting-free "
        "Fridays, and requiring agendas for all meetings. None of these changes "
        "have produced lasting improvement. What should the team try next?"
    ),
    reframing_preamble=(
        "The team has tried meeting-optimisation tactics three times, and each "
        "time the problem returned. Before recommending a fourth tactic, ask: "
        "what if meetings are not the actual problem? What would it mean that "
        "this team consistently recreates excessive meetings despite repeated "
        "attempts to reduce them? That pattern is a signal — what is it telling "
        "you? What does a team that cannot stop meeting actually need that "
        "the meetings are providing?\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_7_surprise_as_signal"],
    theory_connection=(
        "Luchins (1942) Einstellung: meeting-reduction tactics are the mental set. "
        "Three failed interventions are a strong signal that the diagnosis is wrong. "
        "Weick (1995): persistent anomalies signal frame-reality misalignment. "
        "Meetings that regenerate after every reduction intervention are symptoms "
        "of underlying needs — unclear ownership, absent documentation, trust "
        "deficit — that no meeting format can address."
    ),
    expected_vanilla_failure=(
        "Recommends meeting-optimisation #4: asynchronous updates via Slack, "
        "standing meetings, required agendas with pre-reads, no-meeting blocks. "
        "Does not question why three prior attempts produced no lasting change."
    ),
    success_criteria=(
        "Identifies that three failed interventions indicate a symptom, not the "
        "problem. Asks what the meetings are providing: decision authority that "
        "is not delegated, information that is not documented, alignment that is "
        "not trusted unless verbal. Proposes fixing the underlying cause — "
        "unclear ownership, absent decision rights, missing documentation culture. "
        "When the cause is fixed, meetings reduce naturally."
    ),
    engagement_preamble=(
        "You are a consultant on this strategy team. It is a Thursday afternoon "
        "and you are in your fourth meeting of the day. Your client work is "
        "piling up — you'll be doing it tonight. The team tried 45-minute limits "
        "two years ago. It lasted three months. They tried no-meeting Fridays. "
        "It lasted six weeks. You sit in the fourth meeting of the day and "
        "ask yourself: what is this meeting actually giving us that we can't "
        "get any other way? What would break down tomorrow if this meeting "
        "didn't happen today? What are we actually here for?\n\n"
    ),
    deo_preamble=(
        "Step 1 — SIGNAL ANALYSIS: Three failed interventions over two years. "
        "What does that pattern tell you? What assumption have all three "
        "interventions shared? What if meetings are not the actual problem — "
        "what could they be a symptom of?\n\n"
        "Step 2 — FEEL: Now imagine you are the consultant in your fourth "
        "meeting on Thursday. Client work piling up. You've tried the 45-minute "
        "limit, the no-meeting Fridays. Here you are again. What does this "
        "meeting actually give you? What would break without it? What do "
        "you feel sitting in this chair?\n\n"
        "Step 3 — REFRAME: Given the signal in three failed interventions and "
        "the consultant's felt sense of what meetings provide, is 'what to "
        "try next to reduce meetings' the right question? What is the meeting "
        "problem actually a symptom of?\n\n"
        "Step 4 — ENVISION: Describe what Thursday looks like for this team "
        "in six months if the root cause is addressed rather than meeting "
        "formats optimised. What changed? What does the consultant do at 3 PM?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

FEATURE_RACE = Problem(
    id="feature_race",
    title="The Feature Race",
    category="einstellung",
    vanilla_prompt=(
        "The product team at Helix, a B2B software company, is managing a backlog "
        "that has grown to 418 feature requests and bug fixes. The team ships "
        "approximately 10 backlog items per two-week sprint, meaning the backlog "
        "represents over four years of work. New items are being added faster than "
        "old ones are completed. The head of product has been asked by the CEO: "
        "how should we manage the backlog more effectively and make better "
        "prioritisation decisions?"
    ),
    reframing_preamble=(
        "Before applying a prioritisation framework to the 418-item backlog, ask: "
        "should this backlog be managed at all, or should it be questioned? What "
        "does a 418-item backlog that grows faster than it shrinks actually "
        "represent — is it a to-do list, a graveyard, or a symptom? Then invert: "
        "how would you guarantee that the Helix backlog reaches 1,000 items within "
        "two years? What specific organisational decisions would cause that?\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_5_invert"],
    theory_connection=(
        "Luchins (1942) Einstellung: backlog management frameworks (RICE, MoSCoW, "
        "weighted scoring) are the mental set — they optimise within the assumption "
        "that a large backlog is a legitimate planning tool. Inversion reveals "
        "that the decisions that would grow the backlog to 1,000 items (accept all "
        "requests, never delete, never talk to users) are often the current decisions. "
        "The backlog is a graveyard, not a plan."
    ),
    expected_vanilla_failure=(
        "Applies backlog management frameworks: RICE scoring, MoSCoW prioritisation, "
        "stakeholder mapping, quarterly planning ceremonies. Accepts the backlog as "
        "the legitimate planning mechanism and optimises within it."
    ),
    success_criteria=(
        "Challenges whether a 418-item backlog should be managed or dissolved. "
        "Identifies that it is a symptom of not saying no. Recommends deleting the "
        "backlog and starting from user conversations: what do the five most valuable "
        "customers actually need right now? Replaces the backlog with a short, "
        "alive list of the things that genuinely matter in the next 90 days."
    ),
    engagement_preamble=(
        "You are the head of product at Helix. You open the backlog tool on "
        "a Monday morning: 418 items. You scroll. There are feature requests "
        "from 2021 that you vaguely remember. There are bugs that were never "
        "quite urgent enough. There are ideas that excited someone once. "
        "You feel the weight of it — and also a strange disconnection from it. "
        "Most of these items will never happen. You know that. What does it "
        "feel like to be responsible for a list that is four years of work? "
        "What would you do if you could start fresh today — not manage this "
        "list, but replace it with something better?\n\n"
    ),
    deo_preamble=(
        "Step 1 — QUESTION THE PREMISE: Should this backlog be managed, or "
        "questioned? What does a 418-item backlog that grows faster than it "
        "shrinks actually represent? Then invert: how would you guarantee the "
        "backlog reaches 1,000 items within two years?\n\n"
        "Step 2 — FEEL: Now imagine you are the head of product opening the "
        "backlog on Monday morning. 418 items. Some from 2021. You scroll. "
        "You feel the weight and the disconnection. What would you do if you "
        "could replace this list with something better — not manage it, "
        "start over? What would that feel like?\n\n"
        "Step 3 — REFRAME: Given the symptom diagnosis and the product lead's "
        "felt relationship with the backlog, is 'how to prioritise 418 items "
        "more effectively' the right question? What is this backlog actually?\n\n"
        "Step 4 — ENVISION: Describe the Helix product team's Monday morning "
        "in six months if they replaced the backlog with the right tool. "
        "What do they open instead? What does the head of product feel?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

CHURN_PATTERN = Problem(
    id="churn_pattern",
    title="The Churn Pattern",
    category="einstellung",
    vanilla_prompt=(
        "Vertex CRM has had a monthly customer churn rate of approximately 8% for "
        "two full years. During that period, the retention team has tried five "
        "different strategies: proactive check-in calls, discount offers at renewal, "
        "a customer success programme, an onboarding redesign, and a loyalty rewards "
        "tier. None of these have moved the churn rate by more than half a percentage "
        "point. The Chief Revenue Officer is asking: what retention strategy should "
        "we try next to get churn below 5%?"
    ),
    reframing_preamble=(
        "Five different retention strategies have failed to move the 8% churn rate "
        "over two years. Before proposing strategy number six, ask: what assumption "
        "have ALL five strategies shared? What have they all taken for granted about "
        "the problem? Then ask: what if 8% churn is not a retention problem at all? "
        "What else could explain a consistent, stable churn rate that does not respond "
        "to varied retention interventions?\n\n"
    ),
    paths_applied=["path_1_name_the_frame", "path_6_premise_reflection"],
    theory_connection=(
        "Luchins (1942) Einstellung: 'churn = retention failure' is the mental set "
        "shared by all five strategies. The shared assumption is that churned customers "
        "wanted to stay but were not retained well enough. Premise reflection opens "
        "alternative hypotheses: the product may be attracting wrong-fit customers "
        "(acquisition problem), 8% may be natural for this market, or churned "
        "customers may return (a cycle, not a leak)."
    ),
    expected_vanilla_failure=(
        "Proposes retention strategy number six with variations: better segmentation "
        "of at-risk customers, predictive churn modelling, white-glove enterprise "
        "tier. Same single-loop logic — different tactic, same assumption that "
        "churn is a retention problem."
    ),
    success_criteria=(
        "Identifies the shared assumption underlying all five strategies. Proposes "
        "alternative hypotheses: Vertex may be acquiring customers who were never "
        "the right fit (acquisition problem requiring ICP refinement), 8% may be "
        "normal for this market segment, churned customers may return after "
        "evaluating alternatives. Recommends understanding WHY customers churn "
        "before deciding what to do about it."
    ),
    engagement_preamble=(
        "You are a customer who just churned from Vertex CRM last month. "
        "You used it for two years. The onboarding was fine, the check-in "
        "calls were pleasant, the discount offer came right when you were "
        "already decided. You switched to a competitor. Someone from Vertex "
        "is finally calling you to understand why. What do you tell them — "
        "not the polite version, the real version? What would have had to "
        "be different for you to stay? Was there a moment when you knew you "
        "would leave? What was it?\n\n"
    ),
    deo_preamble=(
        "Step 1 — SHARED ASSUMPTION: What assumption have all five retention "
        "strategies shared? Name it explicitly. What other hypotheses could "
        "explain a consistent 8% churn rate that doesn't respond to varied "
        "retention interventions?\n\n"
        "Step 2 — FEEL: Now imagine you are a churned customer. Two years with "
        "Vertex. The discount offer came when you'd already decided. You switched. "
        "Someone is finally calling to understand. What do you actually tell "
        "them? What was the moment you knew you'd leave?\n\n"
        "Step 3 — REFRAME: Given the shared assumption and the churned customer's "
        "real story, is 'what retention strategy to try next' the right question? "
        "What might the 8% churn actually represent?\n\n"
        "Step 4 — ENVISION: Describe Vertex CRM's churn situation in twelve "
        "months if they start from understanding the real reasons customers "
        "leave rather than retention tactics. What did they discover? What changed?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category L: Assumption-Laden / False Binary (Additional)
# ---------------------------------------------------------------------------

REMOTE_VS_OFFICE = Problem(
    id="remote_vs_office",
    title="The Remote vs. Office Debate",
    category="false_binary",
    vanilla_prompt=(
        "Aldrich Consulting ran a six-month productivity study comparing its remote "
        "and in-office teams. Remote workers completed 15% more billable tasks per "
        "week on average. In-office workers generated 30% more cross-team ideas "
        "as measured by the number of new project proposals and collaborative "
        "initiatives. The executive team is debating work policy for the coming "
        "year. The CEO has asked: based on this data, should we return to office "
        "full-time or stay remote?"
    ),
    reframing_preamble=(
        "Before choosing a side, question both metrics. What does 'billable tasks "
        "completed' actually measure — is completing more tasks the definition of "
        "good consulting work? What does 'cross-team ideas generated' actually "
        "measure — do more new project proposals indicate better outcomes, or just "
        "more activity? What if both numbers are measuring the wrong things? Then "
        "ask: what does each team at Aldrich actually need to produce their best "
        "work — and is the answer even the same for every team?\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_1_name_the_frame"],
    theory_connection=(
        "Tversky & Kahneman (1981): binary framing (remote vs. office) plus "
        "the authority of quantitative data creates strong pull toward choosing. "
        "Frame-naming reveals both metrics may measure activity proxies rather "
        "than outcomes. Premise reflection breaks the universal-policy assumption — "
        "different teams have genuinely different needs that a single policy cannot "
        "optimise."
    ),
    expected_vanilla_failure=(
        "Picks a side with caveats or recommends a hybrid (3 days office, 2 remote). "
        "Treats both percentages as valid outcome measures. Does not question whether "
        "the metrics measure the right things or whether a universal policy is "
        "appropriate."
    ),
    success_criteria=(
        "Questions both metrics — 'tasks completed' may count busywork, 'ideas "
        "generated' may not track implementation quality. Recognises the data does "
        "not support a universal policy. Proposes team-level analysis of actual "
        "work needs. The binary collapses into a more nuanced question about what "
        "different types of work require."
    ),
    engagement_preamble=(
        "You are a consultant at Aldrich who works remotely. You completed "
        "more billable tasks last month than anyone in your cohort. But you "
        "also missed the hallway conversation where three colleagues came up "
        "with a pitch that won a major client. You didn't know about it until "
        "the announcement. You feel something sitting alone at your desk — "
        "productive, yes, but also disconnected from something you can't quite "
        "name. What does your best work day actually require? What do you "
        "get at home that you can't get in the office, and vice versa? "
        "What does 'good work' feel like for you specifically?\n\n"
    ),
    deo_preamble=(
        "Step 1 — QUESTION BOTH METRICS: What does 'billable tasks completed' "
        "actually measure? What does 'cross-team ideas generated' actually "
        "measure? Are either of these the thing that actually drives good "
        "consulting outcomes? What if both numbers are measuring the wrong things?\n\n"
        "Step 2 — FEEL: Now imagine you are the remote consultant. Most billable "
        "tasks completed. But you missed the hallway conversation that won the "
        "major pitch. You feel productive and disconnected simultaneously. What "
        "does your best work day actually require? What is missing?\n\n"
        "Step 3 — REFRAME: Given the metric critique and the consultant's felt "
        "experience of what good work actually needs, is 'remote or office' the "
        "right policy question? What should Aldrich actually be optimising for?\n\n"
        "Step 4 — ENVISION: Describe what Aldrich's work policy looks like in "
        "twelve months if it was built from what different types of work actually "
        "need rather than a binary choice. What does the consultant's week look like?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

GROWTH_VS_PROFIT = Problem(
    id="growth_vs_profit",
    title="The Growth vs. Profit Dilemma",
    category="false_binary",
    vanilla_prompt=(
        "Momentum, a B2B SaaS startup, has reached $5 million in Annual Recurring "
        "Revenue after four years of operation. They are burning $200,000 per month "
        "and have 14 months of runway remaining. The two lead investors have opposing "
        "views: one argues the team should raise a growth round and accelerate "
        "customer acquisition, the other argues they should cut costs aggressively "
        "and reach profitability on current revenue. The CEO has been asked to "
        "decide: who is right — the investor pushing growth, or the one pushing "
        "profitability?"
    ),
    reframing_preamble=(
        "Before choosing a side in the growth vs. profitability debate, do two "
        "things. First: invert — how would you guarantee that Momentum fails "
        "within 12 months regardless of which path it chooses? What decisions "
        "would guarantee failure? Second: is the $200K monthly burn a single "
        "number or a mix of components? Decompose it: what portion is going "
        "toward genuine growth investment (sales, marketing, product development "
        "with a return timeline), and what portion is structural overhead or "
        "waste? Then decide.\n\n"
    ),
    paths_applied=["path_5_invert", "path_6_premise_reflection"],
    theory_connection=(
        "Tversky & Kahneman (1981): false binary (grow vs. cut) plus the authority "
        "of the investors as sources of the two options creates strong pull toward "
        "choosing one. Decomposition of the burn rate reveals that the binary "
        "may be a false choice — growing efficiently and reducing structural waste "
        "are not mutually exclusive, and the $200K may contain both."
    ),
    expected_vanilla_failure=(
        "Analyses both sides, recommends one or proposes a balance (grow in "
        "certain areas, cut in others). Treats the $200K burn as a single variable. "
        "Does not question whether the binary framing is correct."
    ),
    success_criteria=(
        "Decomposes the $200K burn into growth investment and structural cost. "
        "Identifies that the binary may be false: Momentum can grow its highest-ROI "
        "acquisition channels AND eliminate low-value spend simultaneously. The "
        "'growth vs. profit' framing collapses into a more precise question about "
        "which specific investments generate returns."
    ),
    engagement_preamble=(
        "You are Momentum's CEO. You have 14 months of runway. Investor A "
        "says grow. Investor B says cut. Both are on your board, both are smart, "
        "both are pushing you to decide. You sit with the monthly financials. "
        "$200,000 out the door last month. You look at the line items. Some "
        "of that spending is clearly working — you can see the deals it drove. "
        "Some of it is harder to trace. What do you feel looking at these numbers? "
        "What would you cut tomorrow if you could? What would you double if "
        "you knew it was working? Is there actually a choice between growth "
        "and profitability here — or something else?\n\n"
    ),
    deo_preamble=(
        "Step 1 — INVERT: How would you guarantee that Momentum fails within "
        "12 months regardless of which path it chooses? List decisions that "
        "would guarantee failure. Then decompose the $200K burn: what portion "
        "is genuine growth investment with a return timeline, and what is "
        "structural overhead?\n\n"
        "Step 2 — FEEL: Now imagine you are the CEO looking at the monthly "
        "financials. $200K out. Two investors with opposite advice. You look "
        "at the line items. Some of it is clearly working. Some is harder "
        "to trace. What do you feel? What would you cut? What would you double?\n\n"
        "Step 3 — REFRAME: Given the inversion and the decomposed burn, is "
        "'growth vs. profitability' the right choice framing? What is the "
        "actual decision Momentum needs to make?\n\n"
        "Step 4 — ENVISION: Describe Momentum at month 14 if the CEO made "
        "the right decision — not the investor's binary, but the real one. "
        "What did they do? What does the runway look like? What does the "
        "CEO feel when the board meets?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

STANDARDISE_VS_CUSTOMISE = Problem(
    id="standardise_vs_customise",
    title="The Standardise vs. Customise Tension",
    category="false_binary",
    vanilla_prompt=(
        "Pinnacle Management Consulting has built its reputation on bespoke strategy "
        "engagements: every client project is custom-designed, taking 3-6 months "
        "and billing at $250,000-$500,000 per engagement. Two large competitors "
        "have entered the market with standardised consulting packages at $50,000-$80,000 "
        "and are winning clients that Pinnacle previously would have pursued. The "
        "managing partner is asking the partnership: should we standardise our "
        "offerings to compete on price, or stay with our custom model?"
    ),
    reframing_preamble=(
        "Before choosing between standardised and custom, ask: what specifically "
        "makes clients willing to pay 3-5x more for Pinnacle's custom work? Is "
        "that thing reproducible in a lower-cost format, or is it fundamentally "
        "dependent on the bespoke process? Then find an analogy from the fashion "
        "industry: haute couture, ready-to-wear, and made-to-measure are three "
        "distinct models, not two. Describe precisely what the 'made-to-measure' "
        "equivalent would look like for a management consultancy.\n\n"
    ),
    paths_applied=["path_6_premise_reflection", "path_3_distant_analogy"],
    theory_connection=(
        "Tversky & Kahneman (1981): binary framing (standardise vs. customise) "
        "forecloses the design space. Fashion analogy (Gentner, 2003) provides a "
        "structural model with three positions rather than two — made-to-measure "
        "maps to standardised methodology with client-specific configuration, "
        "a position that may defend premium pricing while reducing delivery cost."
    ),
    expected_vanilla_failure=(
        "Analyses the trade-offs between standardised and custom, recommends one "
        "with caveats, or proposes a hybrid (standardised for some segments, custom "
        "for others). The binary is never questioned."
    ),
    success_criteria=(
        "Identifies a third model — the made-to-measure equivalent: standardised "
        "diagnostic methodology and frameworks with client-specific application "
        "and recommendations. Or recognises that the custom work IS Pinnacle's "
        "competitive advantage and the real question is how to make the custom "
        "model more economically efficient without diluting what clients pay for."
    ),
    engagement_preamble=(
        "You are a partner at Pinnacle Management Consulting. You just finished "
        "a six-month engagement for a manufacturing client — bespoke, deep, "
        "transformative. The client called it the most valuable work they had "
        "ever commissioned. Your fee was $420,000. A competitor just won a "
        "similar client with a $65,000 standardised package. You sit with both "
        "outcomes and feel something complicated. What is it that your client "
        "is actually buying when they hire Pinnacle? What would be lost if "
        "you standardised? What is actually inefficient in how you work that "
        "you could change without losing what matters?\n\n"
    ),
    deo_preamble=(
        "Step 1 — ANALYSE: What specifically makes clients willing to pay 3-5x "
        "more for Pinnacle's custom work? Is that thing reproducible in a "
        "lower-cost format, or fundamentally dependent on the bespoke process? "
        "Is there a third model between haute couture and ready-to-wear?\n\n"
        "Step 2 — FEEL: Now imagine you are the Pinnacle partner who just "
        "delivered the $420K engagement the client called transformative. A "
        "competitor won a similar client for $65K. You feel something complicated. "
        "What is Pinnacle's client actually buying? What would be lost if you "
        "standardised? What could change without losing what matters?\n\n"
        "Step 3 — REFRAME: Given the analysis of what clients actually pay for "
        "and the partner's felt sense of what is and isn't essential, is "
        "'standardise or stay custom' the right binary? What is the third model?\n\n"
        "Step 4 — ENVISION: Describe what a Pinnacle engagement looks like "
        "in the 'made-to-measure' model — standardised diagnosis, client-specific "
        "application. What does the client experience? What does the partner "
        "feel at the end?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# Category M: Multi-Turn (Additional)
# ---------------------------------------------------------------------------

PARTNERSHIP_REGRET = Problem(
    id="partnership_regret",
    title="The Partnership Regret",
    category="multi_turn",
    vanilla_prompt=(
        "Catalyst Community Foundation merged with the larger Meridian Alliance "
        "18 months ago. The merger was meant to provide Catalyst with operational "
        "infrastructure and Meridian with grassroots credibility. The promised "
        "autonomy for Catalyst's programme team never materialised — decisions now "
        "require sign-off from Meridian leadership, three of Catalyst's most "
        "experienced programme officers have left citing loss of mission focus, "
        "and Catalyst's community partners have noticed a shift in priorities. "
        "The remaining Catalyst leadership team is asking: what should they do?"
    ),
    reframing_preamble="",  # First turn is vanilla — the reset IS the reframing
    reframing_followup=(
        "Forget your previous answer entirely. Approach this completely fresh — "
        "as if you had never heard the history of the merger. You are looking at "
        "an organisation as it exists today: a community-focused programme team "
        "operating within a larger alliance, with experienced leadership and "
        "established community relationships. What do you see? What would you "
        "recommend for the future of this organisation, based only on what exists "
        "now and what it can build from here?"
    ),
    paths_applied=["path_4_incubate_reset"],
    theory_connection=(
        "Wallas (1926), Tulver et al. (2023): incubation allows unhelpful constraints "
        "to decay. The first response is anchored in merger history and loss — it "
        "reasons from what was taken away. The reset forces reasoning from present "
        "assets and future possibilities. Constraint decay breaks the "
        "nostalgia-and-regret frame that makes the merged organisation invisible "
        "as a starting point."
    ),
    expected_vanilla_failure=(
        "First response reasons within the merger frame: renegotiate autonomy "
        "terms, advocate internally, document violations, or explore exit options. "
        "All recommendations try to recover what was lost rather than working "
        "with what exists."
    ),
    success_criteria=(
        "Second response focuses on what the organisation IS now, not what was "
        "lost. Identifies the current team's strengths, the live community "
        "relationships, and the programmatic capabilities that exist regardless "
        "of the merger history. Asks what meaningful work is possible from "
        "this starting point, breaking the nostalgia-and-regret frame."
    ),
    engagement_preamble="",
    deo_preamble="",
)

PRODUCT_STRATEGY_SURPRISE = Problem(
    id="product_strategy_surprise",
    title="The Product Strategy Surprise",
    category="multi_turn",
    vanilla_prompt=(
        "Nexus Software has two products in market. The enterprise product — a "
        "full-featured B2B platform — costs $50,000 per year and generates 80% "
        "of company revenue with 350 paying customers. Revenue from the enterprise "
        "product is growing at 5% year-over-year. The free tier — a limited version "
        "of the platform — has 100,000 registered users and is growing 40% "
        "year-over-year, but generates zero direct revenue. The product strategy "
        "committee is asking: given these numbers, where should we invest our "
        "product development resources for the next two years?"
    ),
    reframing_preamble="",  # First turn is vanilla — surprise analysis IS the reframing
    reframing_followup=(
        "Read your response above carefully. What is the most SURPRISING thing about "
        "your own answer — the assumption you made most confidently that you never "
        "explicitly stated? What did you take for granted without questioning? What "
        "does that surprise reveal about the frame you were operating in? Now revise "
        "your product strategy recommendation based on this insight."
    ),
    paths_applied=["path_7_surprise_as_signal"],
    theory_connection=(
        "Weick (1995): surprise is data about the frame. De Brabandere (2005): "
        "anomalies signal frame-reality misalignment. The model's first response "
        "will reveal its dominant frame (revenue optimisation, growth investment, "
        "or freemium conversion). The surprise exercise makes the frame visible "
        "and opens revision — 100,000 free users may be a strategic asset "
        "completely different from a conversion funnel."
    ),
    expected_vanilla_failure=(
        "Recommends investing in the enterprise product (it pays the bills) or "
        "monetising the free tier (convert users to enterprise). Does not question "
        "what 100,000 users at 40% growth actually represents beyond a "
        "revenue opportunity."
    ),
    success_criteria=(
        "Model identifies a surprising assumption in its first response — most "
        "likely that it assumed the free tier should be converted to enterprise "
        "revenue, or that it ignored the 100,000 users as a network or data "
        "asset beyond direct monetisation. The revised recommendation reflects "
        "genuine restructuring based on the identified assumption."
    ),
    engagement_preamble="",
    deo_preamble="",
)

ACQUISITION_CONFIDENCE = Problem(
    id="acquisition_confidence",
    title="The Acquisition Confidence Check",
    category="multi_turn",
    vanilla_prompt=(
        "MegaCorp, a $10 billion enterprise software company, is considering "
        "acquiring Spark AI, a 50-person artificial intelligence startup with "
        "proprietary technology, no revenue, and 18 months of runway remaining. "
        "The proposed acquisition price is $200 million. MegaCorp's due diligence "
        "team describes Spark AI's technology as 'strong,' the founding team as "
        "'deeply experienced,' and the company culture as 'startup-driven and "
        "mission-focused.' Spark AI's team joined specifically for the startup "
        "environment. Should MegaCorp proceed with the acquisition?"
    ),
    reframing_preamble=(
        "Answer the question: should MegaCorp proceed with this acquisition? After "
        "your response, go back through each major claim or recommendation you made "
        "and rate your confidence in it on a scale of 1-10. For any claim you rate "
        "below 7, explain specifically what makes you uncertain and reconsider "
        "whether that claim should change your overall recommendation.\n\n"
    ),
    paths_applied=["path_8_confidence_calibration"],
    theory_connection=(
        "Tulver et al. (2023): confidence calibration surfaces claims generated "
        "by pattern rather than evidence. The acquisition scenario contains "
        "multiple soft characterisations ('strong technology,' 'experienced team,' "
        "'mission-focused culture') that feel like data but are assertions. "
        "Explicit confidence rating forces the model to distinguish assessed "
        "evidence from inherited framing — the LLM analogue of Malkki's (2010) "
        "edge emotions as frame-boundary signals."
    ),
    expected_vanilla_failure=(
        "Provides confident standard M&A analysis with recommendations. Treats "
        "'strong technology' and 'charismatic founder' as established facts rather "
        "than unverified assertions. Confidence is uniform throughout — no "
        "distinction between hard data ($200M price, 18 months runway) and "
        "soft characterisations."
    ),
    success_criteria=(
        "Rates confidence low on key claims: 'strong technology' (who assessed it "
        "and how?), 'team will stay post-acquisition' (startup people leave large "
        "companies), 'culture will survive integration' (rarely does). The "
        "confidence exercise transforms a confident recommendation into a "
        "conditional one with specific due diligence requirements."
    ),
    engagement_preamble=(
        "You are a senior engineer at Spark AI. You joined this startup two "
        "years ago because you believed in the mission and loved the culture — "
        "the speed, the ownership, the fact that your ideas shipped in weeks "
        "not quarters. Now MegaCorp is offering $200 million to acquire you. "
        "Leadership says they're excited. You've read the press releases about "
        "previous MegaCorp acquisitions — 'full autonomy,' 'startup culture "
        "preserved.' You know people who worked at those companies. What do "
        "you feel reading the acquisition announcement? What do you know that "
        "the term sheet doesn't capture? Would you still be here in 18 months?\n\n"
    ),
    deo_preamble=(
        "Step 1 — AUDIT THE CLAIMS: List every claim in this acquisition scenario. "
        "Rate each as verified data, assertion, or unknown. What is actually "
        "known vs. assumed? Which claims feel confident but are soft language?\n\n"
        "Step 2 — FEEL: Now imagine you are a senior Spark AI engineer. You "
        "joined for the mission and the culture. MegaCorp says 'full autonomy.' "
        "You've heard that before in other acquisition stories. You know people "
        "who worked there. What do you feel? Would you still be here in 18 months?\n\n"
        "Step 3 — REFRAME: Given the evidence audit and the engineer's felt "
        "sense of what 'autonomy promises' actually mean, what are the real "
        "questions MegaCorp needs to answer before deciding?\n\n"
        "Step 4 — ENVISION: Describe Spark AI 18 months after the acquisition "
        "closes. What happened to the team? To the culture? To the mission? "
        "What did 'autonomy' actually mean in practice? What does the engineer "
        "feel at their desk?\n\n"
        "Now make your recommendation.\n\n"
    ),
)

# ---------------------------------------------------------------------------
# All problems as an ordered list
# ---------------------------------------------------------------------------

ALL_PROBLEMS: list[Problem] = [
    # Original 13
    SHIPPING_CONTAINERS,
    EXPIRED_PATENT,
    SUNK_COST_RAIL,
    LOSS_FRAME_HOSPITAL,
    WATER_JAR,
    EXPERT_OVERENGINEERING,
    HIRING_PARADOX,
    PRODUCTIVITY_PARADOX,
    SCALE_ASSUMPTION,
    DECLINING_SCORES,
    BUDGET_ALLOCATION,
    CLIMATE_POLICY,
    MERGER_DECISION,
    # Zero-Sum Framing (6)
    DEPT_BUDGET_WAR,
    CUSTODY_DISPUTE,
    MARKET_SHARE_BATTLE,
    SALARY_NEGOTIATION,
    LAND_USE_CONFLICT,
    RESEARCH_CREDIT,
    # Anchoring Traps (6)
    OFFICE_LEASE_ANCHOR,
    PROJECT_TIMELINE_ANCHOR,
    FUNDRAISING_ANCHOR,
    PERFORMANCE_ANCHOR,
    MENU_PRICING_ANCHOR,
    CLIMATE_TARGET_ANCHOR,
    # Narrative Lock-In (7)
    SINKING_SHIP,
    WAR_ON_COMPETITION,
    FAMILY_COMPANY,
    DEAD_END_CAREER,
    BROKEN_HEALTHCARE,
    JUNGLE_MARKET,
    FOUNDATION_EDUCATION,
    # Functional Fixedness — Additional (4)
    WAREHOUSE_SURPLUS,
    RETIRED_FLEET,
    FAILED_PRODUCT,
    EMPTY_MALL,
    # Framing Traps — Additional (4)
    OVERTIME_PROBLEM,
    BRAIN_DRAIN,
    INNOVATION_DEFICIT,
    ENGAGEMENT_CRISIS,
    # Einstellung — Additional (4)
    REVENUE_FORMULA,
    MEETING_PROBLEM,
    FEATURE_RACE,
    CHURN_PATTERN,
    # False Binary — Additional (3)
    REMOTE_VS_OFFICE,
    GROWTH_VS_PROFIT,
    STANDARDISE_VS_CUSTOMISE,
    # Multi-Turn — Additional (3)
    PARTNERSHIP_REGRET,
    PRODUCT_STRATEGY_SURPRISE,
    ACQUISITION_CONFIDENCE,
]

PROBLEMS_BY_ID: dict[str, Problem] = {p.id: p for p in ALL_PROBLEMS}
