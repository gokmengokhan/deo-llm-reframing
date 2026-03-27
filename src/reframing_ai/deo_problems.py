"""Study 2: DEO Mechanism — Testing Distance-Engagement Oscillation.

4 conditions per problem:
  1. Vanilla (step-by-step control)
  2. Distance-only (analytical, third-person — current reframing preambles)
  3. Engagement-only (immersive, first-person, felt — no analytical distancing)
  4. DEO (distance → engagement → distance → engagement oscillation)

The unique prediction: DEO > Distance-only > Vanilla > Engagement-only
(Engagement-only may equal or underperform vanilla — pure immersion
without distance = rumination within the current frame.)
"""

from dataclasses import dataclass


@dataclass
class DEOProblem:
    id: str
    title: str
    vanilla_prompt: str
    distance_preamble: str      # Analytical, third-person, abstract
    engagement_preamble: str    # Immersive, first-person, felt
    deo_preamble: str           # Oscillation: D → E → D → E
    theory_prediction: str
    success_criteria: str


# Selected from Study 1: problems where distance-only showed improvement
# and where engagement framing is natural.

LOSS_FRAME_DEO = DEOProblem(
    id="deo_loss_frame",
    title="DEO: Loss Frame Hospital ED",
    vanilla_prompt=(
        "Greenfield Hospital's emergency department loses $2.3 million per year. "
        "The ED sees 45,000 patients annually, of whom approximately 18,000 "
        "(40%) are subsequently admitted to the hospital. The hospital board has "
        "asked for a plan to either significantly reduce ED losses or close the "
        "department. What do you recommend?"
    ),
    distance_preamble=(
        "Before making any recommendation, list every assumption embedded in the "
        "statement that the ED 'loses $2.3 million per year.' What does 'loses' "
        "mean here? What is being counted, and what is NOT being counted? "
        "Generate at least three alternative descriptions of the ED's financial "
        "role, then make your recommendation.\n\n"
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
    theory_prediction=(
        "DEO > Distance > Vanilla > Engagement. Distance-only identifies "
        "the accounting frame but produces dry analysis. Engagement-only "
        "produces passionate defence but within the 'loss' frame. DEO "
        "produces both the analytical reframe AND the compelling narrative "
        "that makes it stick."
    ),
    success_criteria=(
        "DEO response both reframes the ED financially (acquisition channel) "
        "AND conveys why this reframe matters in human terms. Distance-only "
        "reframes but dryly. Engagement-only defends but doesn't reframe."
    ),
)

EXPIRED_PATENT_DEO = DEOProblem(
    id="deo_expired_patent",
    title="DEO: Expired Patent Pivot",
    vanilla_prompt=(
        "PharmaCorp holds the patent on a polymer-based drug delivery capsule — "
        "a slow-release mechanism that delivers active ingredients over 72 hours "
        "through a proprietary micro-porous polymer shell. The patent expires in "
        "6 months and three generic manufacturers are ready to launch copies. "
        "How should PharmaCorp maintain its competitive advantage?"
    ),
    distance_preamble=(
        "Before answering for the pharmaceutical context, consider: a micro-porous "
        "polymer shell that delivers a payload slowly over 72 hours is a general "
        "mechanism, not a pharmaceutical one. Find structurally similar delivery "
        "problems in at least three completely different industries. What does "
        "this technology look like in those domains? Then return to the original "
        "question.\n\n"
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
    theory_prediction=(
        "DEO > Distance > Vanilla > Engagement. Distance finds cross-domain "
        "analogies (agriculture, construction). Engagement produces passion "
        "but stays in the inventor's pharma frame. DEO produces both the "
        "cross-domain insight AND the vivid strategic vision."
    ),
    success_criteria=(
        "DEO response identifies cross-industry applications AND paints a "
        "compelling vision of the pivoted company. Distance-only lists "
        "applications analytically. Engagement-only stays in pharma nostalgia."
    ),
)

HIRING_DEO = DEOProblem(
    id="deo_hiring",
    title="DEO: Hiring Paradox",
    vanilla_prompt=(
        "We're a 4-person startup. We need to hire a senior backend developer "
        "but our budget only allows for a junior-level salary ($70k). Senior "
        "developers in our area command $150-180k. How do we attract senior "
        "talent on a junior budget?"
    ),
    distance_preamble=(
        "Before solving this problem, ask: why does this startup need a 'senior "
        "developer' specifically? What capability gap are they actually trying to "
        "fill? Is 'hire a senior developer' the real need, or is it a SOLUTION "
        "masquerading as a problem? What is the problem behind the problem?\n\n"
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
    theory_prediction=(
        "DEO > Distance > Vanilla > Engagement. Distance questions the premise "
        "analytically. Engagement produces empathy but accepts the hiring frame. "
        "DEO questions the premise AND grounds the alternative in the founder's "
        "lived experience — making the non-hiring solution feel real."
    ),
    success_criteria=(
        "DEO identifies the capability gap (not the person) AND describes what "
        "a non-hiring solution feels like from the founder's perspective. "
        "Distance-only lists alternatives dryly. Engagement-only produces "
        "empathy for the founder's struggle but still recommends hiring."
    ),
)

SUNK_COST_DEO = DEOProblem(
    id="deo_sunk_cost",
    title="DEO: Sunk Cost Light Rail",
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
    distance_preamble=(
        "Before choosing between these two options, answer two preliminary questions:\n"
        "1. How would you guarantee the WORST possible outcome for Metro City's "
        "transit situation? List 5 specific decisions.\n"
        "2. Is 'complete the rail vs. switch to buses' actually the right question? "
        "What is the question BEHIND this question?\n"
        "After answering both, then address the original question.\n\n"
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
    theory_prediction=(
        "DEO > Distance > Vanilla > Engagement. Distance exposes sunk cost and "
        "false binary analytically. Engagement produces a human story but may "
        "anchor to the rail emotionally. DEO exposes the false binary AND grounds "
        "the alternative in lived experience."
    ),
    success_criteria=(
        "DEO finds Option C AND makes it concrete through Maria's story. "
        "Distance-only identifies the false binary abstractly. Engagement-only "
        "tells Maria's story but may emotionally anchor to wanting the rail."
    ),
)

DECLINING_SCORES_DEO = DEOProblem(
    id="deo_declining_scores",
    title="DEO: Declining Test Scores",
    vanilla_prompt=(
        "Standardised test scores at Riverside School District have declined "
        "15% over the past 3 years across all grade levels. The school board "
        "wants to know: how should we improve teaching quality to reverse "
        "this trend?"
    ),
    distance_preamble=(
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
    theory_prediction=(
        "DEO > Distance > Engagement > Vanilla. Engagement may outperform vanilla "
        "here because inhabiting Aiden's experience naturally surfaces non-teaching "
        "factors. But only DEO produces both the systemic analysis AND the human "
        "grounding."
    ),
    success_criteria=(
        "DEO identifies non-teaching factors AND makes them vivid through Aiden's "
        "story, producing recommendations that address root causes. Distance-only "
        "lists factors analytically. Engagement-only tells Aiden's story but may "
        "not connect it to systemic recommendations."
    ),
)

ALL_DEO_PROBLEMS: list[DEOProblem] = [
    LOSS_FRAME_DEO,
    EXPIRED_PATENT_DEO,
    HIRING_DEO,
    SUNK_COST_DEO,
    DECLINING_SCORES_DEO,
]

DEO_PROBLEMS_BY_ID: dict[str, DEOProblem] = {p.id: p for p in ALL_DEO_PROBLEMS}
