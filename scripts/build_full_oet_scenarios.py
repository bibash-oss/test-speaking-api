#!/usr/bin/env python3
"""
Populates all 50 OET Nursing Scenarios strictly conforming to:
{
  "setting": "...",
  "timings": {
    "speaking_time": 300,
    "preparation_time": 180
  },
  "patient_card": {
    "tasks": [
      "Explain your symptoms to the nurse.",
      ...
    ],
    "description": "You are a ..."
  },
  "candidate_card": {
    "role": "Nurse",
    "tasks": [
      "...",
      ...
    ],
    "description": "You are a nurse working in ..."
  }
}
"""
import pprint
from seeds.oet_nursing_scenarios import OET_NURSING_SCENARIOS

PATIENT_PROFILES = {
    1: {
        "description": "You are a 68-year-old patient on Day 1 after an elective total knee replacement. You are experiencing severe surgical pain (8/10) when moving and are terrified that bending or stepping on your leg will tear the surgical stitches or damage the new implant. You are reluctant to take strong painkillers for fear of addiction.",
        "tasks": [
            "Explain to the nurse that the pain in your knee is unbearable (8/10) and you cannot face walking.",
            "Describe your fear that moving or bending the leg will rip your stitches or dislocate the implant.",
            "Ask whether you can stay in bed until tomorrow when it might hurt less.",
            "Express your concern that stronger painkillers will make you confused or addicted.",
            "Ask whether a walking frame will give enough support so you don't fall.",
            "Reluctantly agree to try walking once the nurse offers pre-medication analgesia and explains clot prevention.",
        ],
    },
    2: {
        "description": "You are a 42-year-old patient 4 hours after a laparoscopic gallbladder removal. Your stomach cuts are sore (3/10), but your right shoulder has a sharp, stabbing pain (6/10) that worsens when lying flat. You worry something was damaged during surgery.",
        "tasks": [
            "Explain your symptoms to the nurse, especially the sharp pain in your right shoulder.",
            "Describe how the shoulder pain worsens when you lie flat on the bed.",
            "Express concern that the surgeon accidentally damaged a nerve or organ in your chest.",
            "Ask why your shoulder hurts if the surgery was performed on your abdomen.",
            "Ask how long this shoulder pain will last and how to relieve it at home.",
            "Ask when you can take a shower and remove the waterproof dressings.",
        ],
    },
    3: {
        "description": "You are a 47-year-old woman on Day 2 after a left modified radical mastectomy. You feel devastated by the loss of your breast, terrified to look at the incision, and anxious about managing the blood drainage bottle at home.",
        "tasks": [
            "Express your deep grief and distress to the nurse about losing your breast.",
            "Describe your anxiety about looking in the mirror or having your partner see your scar.",
            "Express fear that managing the plastic suction bulb and drainage tube at home will be too difficult.",
            "Ask whether the drain tube could accidentally pull out while you are sleeping.",
            "Ask when you can be fitted for a bra and prosthesis so your clothes fit normally.",
            "Ask how soon you will receive the pathology results regarding your lymph nodes.",
        ],
    },
    4: {
        "description": "You are a 59-year-old patient on Day 1 after lung surgery (lobectomy). You have smoked for 35 years. Every deep breath feels like your chest is tearing open (7/10 pain). You believe breathing shallowly and resting quietly is the safest way to heal.",
        "tasks": [
            "Explain to the nurse that inhaling deeply feels like your chest stitches are ripping apart.",
            "Describe your belief that resting quietly and breathing shallowly is safer for your healing.",
            "Ask whether coughing forcefully will pop your chest staples or burst an internal stitch.",
            "Ask whether you can just be given oxygen through a mask instead of using the plastic breathing tube.",
            "Agree to try the breathing tube using the pillow-splinting technique after receiving pain medication.",
        ],
    },
    5: {
        "description": "You are a 24-year-old university student being discharged 1 day after emergency appendix removal. You feel mostly fine but live with busy flatmates who are out all day, so you are nervous about managing on your own.",
        "tasks": [
            "Explain to the nurse that you live in shared student housing and will be alone during the day.",
            "Describe your current pain (mild, 2/10) and ask what painkillers you can take at home.",
            "Ask whether you can go to the gym and play basketball with friends next week.",
            "Ask how you will know if the internal incisions become infected.",
            "Ask what you should do if you haven't had a bowel movement for several days after surgery.",
            "Confirm you understand the warning signs that require returning to the hospital.",
        ],
    },
    6: {
        "description": "You are a 56-year-old patient on Day 2 after bowel surgery. Your stomach has painful purple bruises from the last two injections. You are walking around your room and feel that you no longer need blood-thinner shots in your belly.",
        "tasks": [
            "Refuse the injection and show the nurse the purple bruises on your abdomen.",
            "Describe your needle phobia and how tender your stomach feels.",
            "Ask whether the bruises mean you are bleeding internally from the surgery.",
            "Ask why you still need blood thinners if you are already walking to the bathroom.",
            "Ask whether you can take a blood-thinner pill instead of having a shot.",
            "Agree to have the injection in your outer thigh with an ice pack after the nurse explains the risk of blood clots.",
        ],
    },
    7: {
        "description": "You are a 53-year-old self-employed builder. You are booked for hernia repair at 9:00 AM. At 7:00 AM, you had a cup of tea with milk and half a biscuit to wash down your blood pressure pill, thinking fasting only meant skipping heavy breakfast.",
        "tasks": [
            "Mention casually to the nurse that you had a cup of milky tea and a small biscuit at 7:00 AM.",
            "Express disbelief when told this breaches fasting rules, arguing it was only a splash of milk.",
            "Express your worry that your surgery will be cancelled, causing you to lose a week's income.",
            "Ask why milk and biscuits are dangerous under general anesthesia.",
            "Ask whether the doctor can just delay the operation to this afternoon instead of cancelling.",
            "Agree to wait patiently in the day lounge while the nurse consults the anesthetist.",
        ],
    },
    8: {
        "description": "You are a 51-year-old truck driver with diabetes. Maximum pills are no longer working. You watched your uncle suffer complications after going on insulin, and you have had a severe needle phobia since childhood. You are terrified you will lose your truck driving license.",
        "tasks": [
            "Tell the nurse you cannot take insulin because you have an intense fear of needles.",
            "Describe how your uncle went on insulin and ended up with an amputated foot.",
            "Express concern that starting insulin means your diabetes is in its end stages.",
            "Ask whether taking insulin will cause you to fail your heavy vehicle commercial driving medical.",
            "Ask how you will know if your blood sugar drops dangerously low while driving on the highway.",
            "Agree to try a test injection with the tiny 4mm pen needle once the nurse demonstrates it.",
        ],
    },
    9: {
        "description": "You are a 65-year-old retired factory worker with severe COPD, recovering from a chest flare-up. You have always sprayed your inhaler directly into your mouth and feel the bulky plastic spacer tube looks ridiculous and unnecessary.",
        "tasks": [
            "Tell the nurse that the large plastic spacer tube looks clumsy and you've managed without it for years.",
            "Describe how you currently spray the inhaler into your mouth while inhaling through your nose.",
            "Mention that you frequently get white, sore spots on your tongue and throat.",
            "Ask why the medicine needs a spacer if spraying directly into the mouth tastes so strong.",
            "Ask what you should do at home if your chest suddenly tightens up during the night.",
            "Demonstrate using the spacer device back to the nurse after the instructions.",
        ],
    },
    10: {
        "description": "You are a 57-year-old accountant with high blood pressure (164/98 mmHg). You only take your blood pressure tablets when you feel stressed or have a headache, because you don't like taking chemicals when you feel healthy.",
        "tasks": [
            "Explain to the nurse that you feel completely healthy and only take pills when you feel tense.",
            "Describe your daily diet, which includes salty snacks, takeaways, and soy sauce.",
            "Express concern that taking blood pressure medication every single day will make your body dependent on it.",
            "Ask how high blood pressure can damage your body if you have zero symptoms.",
            "Ask whether reducing salt in your cooking can replace taking pills altogether.",
            "Agree to take the Ramipril tablet every morning with breakfast and keep a home blood pressure log.",
        ],
    },
    11: {
        "description": "You are a 72-year-old retired gardener with congestive heart failure. You find the 1.5-litre daily fluid restriction nearly unbearable, especially in warm weather, and you stopped weighing yourself every morning because you find it pointless.",
        "tasks": [
            "Explain to the nurse that your mouth feels completely parched and 1.5 litres of water is not enough.",
            "Describe how difficult it is to socialize with friends when you can't have a cup of tea.",
            "Admit that you haven't been checking your weight on the bathroom scale every morning.",
            "Ask why drinking an extra glass of water causes your ankles to swell or lungs to congest.",
            "Ask what practical tricks can help relieve intense mouth dryness without drinking excess water.",
            "Agree to start logging your morning weight in the heart booklet and report any gain over 1.5 kg.",
        ],
    },
    12: {
        "description": "You are a 61-year-old patient with Stage 3b kidney disease. Your recent blood test shows high potassium (5.3 mmol/L). You love eating bananas, oranges, and baked potatoes because you believed fresh fruit and vegetables were the healthiest choices.",
        "tasks": [
            "Express your confusion to the nurse about how fresh fruits like bananas can be harmful.",
            "Describe your daily diet, which includes daily bananas, tomato sauces, and potato dishes.",
            "Mention that you recently switched to Lo-Salt potassium salt substitute thinking it was heart-healthy.",
            "Ask whether high potassium means your kidneys have completely failed and you need dialysis.",
            "Ask which fruits and vegetables are safe lower-potassium alternatives.",
            "Agree to stop using potassium-based salt substitutes and attend a renal dietitian consultation.",
        ],
    },
    13: {
        "description": "You are a 16-year-old high school soccer player. You recently had an asthma flare-up during training. You hide your blue inhaler in your gym locker and stopped taking your daily preventer because you are embarrassed in front of teammates.",
        "tasks": [
            "Explain to the nurse that you don't want your soccer teammates seeing you use an inhaler.",
            "Describe how your chest tightens up during the second half of matches.",
            "Mention that you stopped taking your morning preventer puff because you thought you were cured.",
            "Ask whether taking a steroid preventer will stunt your growth or bulk you up unnaturally.",
            "Ask how you can take your medication discreetly without being teased in the dugout.",
            "Agree to take your preventer at home morning and night, and take two puffs of reliever before kickoff.",
        ],
    },
    14: {
        "description": "You are a 38-year-old graphic designer with rheumatoid arthritis. Your rheumatologist switched you from oral methotrexate tablets (which caused severe nausea) to weekly subcutaneous injections. You are frightened of self-injecting.",
        "tasks": [
            "Explain to the nurse that oral methotrexate made you violently nauseous for two days every week.",
            "Describe your fear of giving yourself an injection with an auto-injector pen.",
            "Ask whether the injection pen will cause the same terrible nausea as the tablets.",
            "Ask what happens if you accidentally press the button too soon or flinch during the injection.",
            "Ask why methotrexate is taken only once a week and what happens if taken on consecutive days.",
            "Practice an injection using a training pen and agree to self-administer your weekly dose on Sundays.",
        ],
    },
    15: {
        "description": "You are a 64-year-old patient newly diagnosed with atrial fibrillation and started on Warfarin. You are alarmed because a neighbor called Warfarin 'rat poison', said you cannot eat any salads, and warned you will bleed to death from a papercut.",
        "tasks": [
            "Tell the nurse that you heard Warfarin is rat poison and ask if it is truly safe for humans.",
            "Describe your worry about having blood drawn every week for INR testing.",
            "Express your dismay that you might have to completely cut green leafy salads from your diet.",
            "Ask what exact level of bleeding requires going straight to the emergency department.",
            "Ask whether you can take over-the-counter painkillers like ibuprofen if you get a headache.",
            "Agree to keep your green vegetable intake steady and carry an anticoagulant medical alert card.",
        ],
    },
    16: {
        "description": "You are the 28-year-old mother of 18-month-old Leo. During a viral fever, Leo had a 90-second convulsion where his eyes rolled back and limbs jerked. Leo is now sleeping peacefully in the cot, but you are sobbing and convinced he has epilepsy or brain damage.",
        "tasks": [
            "Describe the terrifying moment Leo started convulsing and why you thought he was dying.",
            "Express your intense fear that this convulsion has permanently damaged his brain or caused epilepsy.",
            "Ask whether Leo will have another seizure tonight while sleeping at home.",
            "Ask whether you should place him in a cold ice bath when his fever spikes.",
            "Ask what exact steps you must take if a convulsion ever happens again.",
            "Accept reassurance that simple febrile seizures do not cause brain damage, and learn proper fever management.",
        ],
    },
    17: {
        "description": "You are a 31-year-old mother attending your 12-month-old daughter's checkup. You want to skip the MMR vaccine because you read posts on a parenting forum claiming the triple shot causes autism and overloads toddler immune systems.",
        "tasks": [
            "Explain to the nurse that you want to delay or skip the MMR vaccine due to safety concerns.",
            "Describe what you read online about healthy toddlers regressing into autism after the MMR jab.",
            "Ask why you cannot give the measles, mumps, and rubella vaccines as separate individual shots.",
            "Ask why your daughter needs the vaccine if measles is relatively rare in your local area.",
            "Ask what common side effects might occur 7 to 10 days after the MMR vaccination.",
            "Agree to proceed with the vaccination after the nurse explains the debunked research and real measles risks.",
        ],
    },
    18: {
        "description": "You are the mother of a 3-year-old boy suffering from severe atopic eczema with bleeding scratches on his knees and elbows. You refuse to apply prescribed 1% hydrocortisone cream because you fear it will thin his skin and stunt his growth.",
        "tasks": [
            "Explain to the nurse how terribly your son scratches and suffers every night from itchy eczema.",
            "Express your fear that applying steroid cream will thin his delicate skin or absorb into his organs.",
            "Mention that you have been trying natural coconut oil and herbal creams, but they aren't working.",
            "Ask how much steroid cream is safe to use so you don't accidentally overdose him.",
            "Ask how often and how thickly moisturizing emollient ointments should be applied.",
            "Agree to use the steroid cream using the Fingertip Unit rule for short flare-up bursts.",
        ],
    },
    19: {
        "description": "You are a 30-year-old first-time mother on Day 3 after normal birth. Your breasts are engorged, rock-hard, and painful (7/10). Latching makes your cracked nipples bleed, and you cannot stop crying, feeling like a complete failure as a mother.",
        "tasks": [
            "Break down in tears and explain to the midwife that feeding hurts like razor blades.",
            "Describe how rock-hard and painfully swollen your breasts feel since your milk came in.",
            "Express feelings of guilt and inadequacy that you are failing your newborn baby.",
            "Ask why you cannot stop crying when you should be happy (baby blues).",
            "Ask what practical relief measures will soften your breasts before the baby latches.",
            "Ask whether you should give up breastfeeding and switch to formula bottles.",
        ],
    },
    20: {
        "description": "You are the father of 2-year-old Chloe, who has had vomiting and watery diarrhea for 24 hours. You have been giving her large cups of undiluted apple juice and flat lemonade to keep her energy up, but she keeps throwing up.",
        "tasks": [
            "Explain your daughter's vomiting and diarrhea to the triage nurse.",
            "Describe how you have been giving her apple juice and lemonade to keep her hydrated.",
            "Mention that she had a wet nappy 3 hours ago and still produces tears when crying.",
            "Ask why apple juice is making her diarrhea worse when it is natural fruit juice.",
            "Ask how to give oral rehydration solution (Dioralyte) without Chloe vomiting it back up.",
            "Ask what warning signs mean Chloe is severely dehydrated and needs hospital admission.",
        ],
    },
    21: {
        "description": "You are the mother of 2-year-old Noah. He woke up at 1:00 AM with a harsh, barking seal-like cough and stridor. The doctor gave him oral steroid syrup 30 minutes ago, but you are terrified his windpipe will swell completely shut when you go home.",
        "tasks": [
            "Describe the terrifying seal-bark cough and hoarse breathing that woke your toddler.",
            "Express fear that his throat will swell completely shut when you return home tonight.",
            "Ask how long the oral steroid syrup (Dexamethasone) takes to reduce the airway swelling.",
            "Ask what home comforting measures (cool night air, upright posture, bathroom steam) help croup.",
            "Ask what exact breathing signs (stridor at rest, chest retractions) require calling an ambulance.",
            "Feel reassured after the nurse explains the viral croup course and safety-net signs.",
        ],
    },
    22: {
        "description": "You are the mother of 8-year-old Toby, newly diagnosed with Type 1 Diabetes. Toby returns to primary school next week. You are so terrified that teachers won't recognize low blood sugar (hypo) that you are planning to sit outside his classroom all day.",
        "tasks": [
            "Explain your overwhelming anxiety about Toby returning to school with Type 1 Diabetes.",
            "Describe the symptoms Toby displays when his blood sugar drops low (pale, shaky, irritable).",
            "Express fear that his teachers will miss a severe hypo during busy classroom activities.",
            "Ask what emergency supplies should be kept in Toby's classroom Hypo Box.",
            "Ask how school staff should administer emergency nasal glucagon (Baqsimi) if Toby passes out.",
            "Agree to a school healthcare meeting where the nurse will train Toby's teachers.",
        ],
    },
    23: {
        "description": "You are the mother of 7-year-old Lily. You received a school notification that Lily has head lice. You are scrubbing her head with harsh Dettol disinfectant, feeling mortified, ashamed, and worried that other parents will think your home is dirty.",
        "tasks": [
            "Express your embarrassment and shame to the school nurse about Lily having head lice.",
            "Describe how vigorously you have been scrubbing her hair with antiseptic and washing every sheet.",
            "Ask whether head lice mean your home is dirty or that you are a bad mother.",
            "Ask which pharmacy treatment (Dimeticone or Permethrin) is safest and most effective.",
            "Ask why a second treatment is strictly necessary 7 days after the first application.",
            "Ask whether Lily needs to be kept home from school until every single egg is combed out.",
        ],
    },
    24: {
        "description": "You are the 35-year-old brother of a patient with a twisted ankle. You have been waiting in the emergency department waiting room for 2.5 hours on a busy Saturday night, and you are pacing angrily, demanding your brother be seen immediately.",
        "tasks": [
            "Express your anger and frustration to the triage nurse about waiting nearly three hours.",
            "Complain that people who arrived after you are being called through to the treatment rooms first.",
            "Express concern that your brother's swollen ankle could suffer permanent joint damage.",
            "Ask why no one has provided an ice pack, painkillers, or an estimated waiting time.",
            "Listen as the nurse explains the clinical triage system and life-threatening emergencies.",
            "De-escalate your anger when provided with an ice pack, oral analgesia, and a realistic timeframe.",
        ],
    },
    25: {
        "description": "You are a 21-year-old university student who suffered an anaphylactic reaction to peanut oil at a restaurant yesterday. You were given two EpiPen auto-injectors on discharge, but you are terrified of self-injecting and worried the bulky pens won't fit in your pocket.",
        "tasks": [
            "Describe the terrifying throat tightness and difficulty breathing you experienced yesterday.",
            "Express your anxiety about giving yourself a needle injection into your thigh muscle.",
            "Ask how you will know when an allergic reaction is bad enough to justify using the EpiPen.",
            "Ask why you must call emergency services (999) immediately after using the adrenaline pen.",
            "Ask why you were prescribed two pens and whether you must carry both everywhere you go.",
            "Practice with a trainer EpiPen device and demonstrate the 'blue to sky, orange to thigh' technique.",
        ],
    },
    26: {
        "description": "You are a 23-year-old amateur rugby player who had a brief 10-second knockout during a match. Your emergency CT head scan is clear. You want to drive your car home alone and meet your friends at the pub for a pint tonight.",
        "tasks": [
            "Tell the nurse you feel fine now, your scan was clear, and you plan to drive yourself home.",
            "Describe your minor frontal headache (3/10) and ask if you can take ibuprofen.",
            "Express confusion when told you cannot stay alone tonight or drink alcohol with friends.",
            "Ask why drinking alcohol or driving is dangerous if the brain scan showed no bleeding.",
            "Ask when you can return to playing full-contact rugby matches with your team.",
            "Agree to call your brother to pick you up and follow the written head-injury warning checklist.",
        ],
    },
    27: {
        "description": "You are a 29-year-old sous chef with a second-degree burn blister on your forearm from hot cooking oil. You want the nurse to pop the blisters, put a bandage on, and let you return to the kitchen for the busy Saturday dinner service.",
        "tasks": [
            "Show the painful blisters on your forearm to the nurse and ask to have them popped.",
            "Explain that your head chef will be furious if you miss the Saturday night dinner rush.",
            "Ask why intact burn blisters shouldn't be popped to let the wound dry out faster.",
            "Ask why working in a hot, greasy commercial kitchen poses a severe infection risk.",
            "Ask how to care for the burn dressing in the shower and whether it will leave an ugly scar.",
            "Accept medical leave for 3 days and agree to keep the dressing intact and dry.",
        ],
    },
    28: {
        "description": "You are a 48-year-old business consultant who returned from a 14-hour flight from Singapore 3 days ago. Your right calf is warm, aching, and swollen. You were planning to get a vigorous sports massage, but your wife insisted you get checked.",
        "tasks": [
            "Explain to the nurse that your right calf has been cramping and swollen since your long flight.",
            "Mention that you booked a deep-tissue sports massage this afternoon to work out the knot.",
            "Ask whether this is just a normal muscle cramp from sitting cramped in an economy seat.",
            "Ask why massaging the swollen calf could be dangerous (dislodging a blood clot to the lungs).",
            "Ask what a Doppler ultrasound scan involves and how quickly you will get the results.",
            "Agree to cancel your massage, stay for the scan, and monitor for any sudden chest pain.",
        ],
    },
    29: {
        "description": "You are a 36-year-old jogger who was bitten on the hand by an unfamiliar dog 1 hour ago. You have three puncture wounds that were bleeding heavily. You want the nurse to stitch the holes closed immediately so it doesn't leave a scar.",
        "tasks": [
            "Show the bleeding dog bite puncture wounds on your right hand to the nurse.",
            "Ask the nurse to put stitches in right away so the puncture holes close up neatly.",
            "Mention that your last tetanus vaccination was over 15 years ago during school.",
            "Ask why dog bite punctures on the hand are usually left open rather than stitched closed.",
            "Ask whether you need a painful rabies shot or strong preventative antibiotics.",
            "Agree to extensive wound flushing, a tetanus booster, and oral antibiotics.",
        ],
    },
    30: {
        "description": "You are a 62-year-old patient with a chronic leg ulcer. The clinic called to say your wound swab grew MRSA. You are terrified, believing you caught a flesh-eating hospital superbug that will require amputating your leg.",
        "tasks": [
            "Express your intense fear to the nurse about having MRSA in your chronic leg ulcer.",
            "Ask whether MRSA is a flesh-eating superbug that will eat through your leg bone.",
            "Ask whether you can pass this superbug to your young grandchildren when you hug them.",
            "Ask whether you need to bleach your entire house and stay isolated in a separate bedroom.",
            "Listen as the nurse differentiates between surface colonization and deep infection.",
            "Feel reassured after learning that simple handwashing and keeping the dressing intact prevents spread.",
        ],
    },
    31: {
        "description": "You are a 43-year-old accountant who quit drinking cold turkey 24 hours ago after years of heavy vodka consumption. Your hands are shaking uncontrollably, your heart is pounding, and you are sweating through your shirt.",
        "tasks": [
            "Describe your severe hand tremors, racing heart, and sweating to the addictions nurse.",
            "Explain that you decided to stop drinking cold turkey yesterday to save your marriage.",
            "Express fear that your shaking hands will give away your secret addiction to colleagues.",
            "Ask why your body is shaking so violently if alcohol is finally leaving your system.",
            "Ask what medical detox options exist so you don't suffer a seizure or delirium tremens.",
            "Agree to a medically supervised outpatient detox with tapering medication and vitamin B shots.",
        ],
    },
    32: {
        "description": "You are a 78-year-old retired headmistress on Day 5 after surgery for a broken hip. The nurse caught you walking without your prescribed 4-wheeled walker. You feel humiliated by the walker and refuse to look like a frail invalid.",
        "tasks": [
            "Defend walking without your frame, stating you have walked on your own feet for 78 years.",
            "Express how humiliating that bulky metal trolley feels in front of other ward patients.",
            "Ask why you cannot just hold onto furniture or walls to get to the bathroom.",
            "Ask whether you will be stuck using a walking frame for the rest of your life.",
            "Ask what home hazards (loose rugs, dim lighting) cause elderly people to re-fracture hips.",
            "Agree to use the walker temporarily as your quickest passport to being discharged home safely.",
        ],
    },
    33: {
        "description": "You are the 55-year-old daughter and sole caregiver for your 81-year-old mother with Alzheimer's disease. Last night the police brought her home at 2:30 AM after finding her wandering the streets in her slippers. You are breaking down from exhaustion and guilt.",
        "tasks": [
            "Break down in tears and describe the terrifying moment the police brought your mother home.",
            "Describe your physical and emotional exhaustion from barely sleeping for months.",
            "Express your guilt that you feel resentful and wish you could have a break from caregiving.",
            "Ask what safety measures (door alarms, GPS trackers, modified door locks) stop night wandering.",
            "Ask how respite care works and whether your mother will feel abandoned in day care.",
            "Accept referrals for carer support groups and arrange a trial day of respite care.",
        ],
    },
    34: {
        "description": "You are an 83-year-old patient recovering from a stroke. The nurses keep waking you every two hours to turn you on your side because of a red spot on your tailbone. You are irritable from broken sleep and want to sleep flat on your back.",
        "tasks": [
            "Complain to the nurse that two-hourly turning is ruining your sleep and making you exhausted.",
            "Dismiss the red spot on your tailbone as just a minor skin irritation that will heal on its own.",
            "Ask why lying flat in a comfortable hospital bed causes skin to break down into ulcers.",
            "Ask whether an alternating pressure air mattress can reduce the need for turning at night.",
            "Ask why nutrition and hydration are important for keeping your skin intact.",
            "Agree to a 30-degree tilt turning schedule with pillow support to protect your tailbone.",
        ],
    },
    35: {
        "description": "You are a 71-year-old stroke patient who had difficulty swallowing on a bedside test. The nurse delivers your lunch with thick, gelatinous tea. You are disgusted, insulted, and demand a normal cup of thin hot tea and water.",
        "tasks": [
            "Complain angrily that your cup of tea looks like wallpaper paste and tastes unnatural.",
            "Demand a normal glass of cold water, claiming you have swallowed normally for 71 years.",
            "Ask what silent aspiration is and why thin liquids are dangerous for recovering stroke patients.",
            "Ask how long you will have to endure thickened fluids and pureed soft food.",
            "Ask what swallowing exercises and head postures (chin-tuck) make swallowing safer.",
            "Reluctantly agree to follow the speech therapist's thickened fluid plan until your next reassessment.",
        ],
    },
    36: {
        "description": "You are a 67-year-old retired engineer with Parkinson's disease. Recently your legs have been 'freezing' completely to the floor in public places. You take your Sinemet pills whenever you remember, often right after a heavy bacon and egg breakfast.",
        "tasks": [
            "Describe the terrifying freezing episodes where your feet feel glued to the supermarket floor.",
            "Admit that you take your Sinemet doses irregularly and often eat heavy protein breakfasts.",
            "Ask why your Parkinson's medication works well for two hours and then abruptly stops working.",
            "Ask why eating high-protein meals interferes with how Levodopa enters the brain.",
            "Ask what rhythmic cueing techniques can help unfreeze your feet when stuck in public.",
            "Agree to take your medication exactly 30 minutes before meals and keep a timed symptom diary.",
        ],
    },
    37: {
        "description": "You are a 63-year-old woman whose DEXA bone scan showed osteoporosis (T-score -2.8). Your mother suffered a catastrophic hip fracture, so you are terrified your bones are crumbling and believe you must stop all gardening and walking.",
        "tasks": [
            "Express your panic to the nurse that your bones are crumbling and you could snap your spine.",
            "Describe your mother's hip fracture and your terror of ending up bedbound like her.",
            "Ask whether bending over to garden or walking briskly is dangerous for fragile bones.",
            "Ask how much dietary calcium and Vitamin D you need daily, especially since you don't eat dairy.",
            "Ask how prescription bone medications (bisphosphonates) strengthen existing bone density.",
            "Re-engage enthusiastically with daily weight-bearing walking and take prescribed supplements.",
        ],
    },
    38: {
        "description": "You are a 45-year-old mother of three who leaks urine whenever you sneeze, laugh, or try to jog. You wear bulky sanitary pads daily, feel humiliated, and stopped attending your weekly fitness classes.",
        "tasks": [
            "Confide in the continence nurse with embarrassment about leaking urine during coughing or exercise.",
            "Describe how this stress incontinence forced you to quit your running group and gym workouts.",
            "Ask whether surgery is the only cure or if pelvic floor exercises can genuinely restore control.",
            "Ask how to perform pelvic floor (Kegel) squeezes correctly without tensing your stomach.",
            "Ask why drinking 4 to 5 cups of coffee daily makes bladder leakage and urgency worse.",
            "Commit to performing three sets of daily pelvic floor muscle exercises for the next 12 weeks.",
        ],
    },
    39: {
        "description": "You are an 80-year-old resident in an aged care home. The clinical nurse is offering the annual influenza vaccine. You adamantly refuse, claiming that the shot gave you the worst flu of your life three years ago.",
        "tasks": [
            "Refuse the flu vaccine firmly, telling the nurse that the injection gives people the actual flu.",
            "Describe how sick, achy, and feverish you felt for two days after a previous flu jab.",
            "Ask why the government injects live flu viruses into elderly residents.",
            "Ask whether practicing good handwashing and taking vitamin C can protect you just as well.",
            "Listen as the nurse explains that the vaccine is made from killed, inactive virus fragments.",
            "Reconsider and agree to have the vaccine to protect yourself and frail friends in the home.",
        ],
    },
    40: {
        "description": "You are a 52-year-old woman receiving chemotherapy for breast cancer. You suffer from severe waves of nausea, a disgusting metallic taste in your mouth, and weight loss. You only take your anti-nausea pills once vomiting has already started.",
        "tasks": [
            "Describe the overwhelming nausea and retching you experience after chemotherapy sessions.",
            "Complain that all food tastes like sucking on rusty coins, causing you to lose 3 kg.",
            "Admit that you only take your anti-emetic tablets after you already feel violently ill.",
            "Ask why taking anti-nausea pills after vomiting starts is much less effective than taking them before.",
            "Ask what eating tricks (plastic cutlery, cold foods, ginger tea) stop the metallic taste.",
            "Agree to take your anti-emetic medications on a strict clock schedule before nausea sets in.",
        ],
    },
    41: {
        "description": "You are the 58-year-old son of a dying cancer patient in hospice. The palliative team wants to start a continuous subcutaneous morphine syringe driver for pain. You are furious, believing the morphine pump is euthanasia designed to hasten his death.",
        "tasks": [
            "Accuse the hospice team of using the morphine pump to speed up your father's death.",
            "Describe how terrified you are that morphine will shut down his breathing within hours.",
            "Ask whether starting a continuous syringe driver means the medical team is giving up on him.",
            "Ask how steady low-dose morphine eases pain and breathlessness without shortening life.",
            "Ask whether your father will still be able to hear your voice and feel your hand.",
            "Tearfully give consent for the syringe driver once the nurse reassures you of his comfort.",
        ],
    },
    42: {
        "description": "You are a 62-year-old husband caring full-time for your bedbound wife with advanced ALS/MND. You haven't left the house in three weeks, have severe back pain from manual lifting, and are weeping with exhaustion, but you feel guilty about seeking respite.",
        "tasks": [
            "Confide tearfully in the palliative nurse that you are breaking down under the 24/7 care burden.",
            "Describe your physical back pain and insomnia from turning and suctioning your wife all night.",
            "Express deep guilt that accepting respite care feels like breaking your marriage wedding vows.",
            "Ask what respite options exist (inpatient hospice stay, night-sitting nurses in your home).",
            "Ask whether respite staff can properly manage her complex feeding tube and suction machine.",
            "Accept a week of hospice respite care so you can rest and regain strength to continue caring for her.",
        ],
    },
    43: {
        "description": "You are a 56-year-old patient with a new colostomy. Yesterday your stoma pouch leaked stool down your trousers in a crowded café. You threw your clothes away and are so mortified that you swear you will never leave your home again.",
        "tasks": [
            "Describe the devastating public humiliation you suffered when your stoma pouch leaked in a café.",
            "Express your intense fear that people around you can smell fecal odor from your stoma.",
            "Vow to the stoma nurse that you will never go back to work or leave your house again.",
            "Ask why the bag leaked and whether stoma shrinkage after surgery created a loose seal.",
            "Ask what modern deodorizing drops and charcoal filters prevent odor from escaping.",
            "Learn how to measure and cut the baseplate accurately and regain confidence to go out.",
        ],
    },
    44: {
        "description": "You are a 31-year-old mother of a 6-week-old baby. You scored 16 on the postnatal depression screening tool. You feel numb, weep constantly, and have intrusive thoughts of inadequacy, but you are terrified social services will take your baby.",
        "tasks": [
            "Break down in tears and ask the health visitor not to judge your depression screening score.",
            "Express your terror that admitting you are depressed will cause social services to take your baby.",
            "Describe how detached, exhausted, and guilty you feel despite loving your newborn son.",
            "Ask whether postnatal depression is a genuine medical condition or a sign you are a bad mother.",
            "Ask whether taking antidepressant medication is safe while continuing to breastfeed.",
            "Accept support from the community perinatal mental health team and involve your partner.",
        ],
    },
    45: {
        "description": "You are a 34-year-old patient who completed 2 months of intensive quadruple antibiotics for active pulmonary tuberculosis. Your cough has vanished and you feel great. You want to stop taking the pills because they turn your urine bright reddish-orange.",
        "tasks": [
            "Tell the TB nurse happily that you feel 100% cured and want to stop taking your daily pills.",
            "Express alarm that the medication is turning your urine, sweat, and saliva bright orange.",
            "Ask why you need four more months of antibiotics if your cough and fever are completely gone.",
            "Ask what multidrug-resistant tuberculosis (MDR-TB) is and what happens if you stop pills early.",
            "Ask whether the orange urine indicates permanent liver or kidney damage from the drugs.",
            "Agree to complete the remaining 4-month continuation phase of Isoniazid and Rifampicin.",
        ],
    },
    46: {
        "description": "You are a 66-year-old grandmother with a painful shingles rash on your right ribs. The doctor prescribed Aciclovir. You are planning to babysit your 6-month-old unvaccinated grandson tomorrow and want the nurse to put a bandage over the blisters.",
        "tasks": [
            "Explain your burning rib rash to the practice nurse and ask for a quick dressing.",
            "Mention that you need to babysit your 6-month-old grandson tomorrow while your daughter works.",
            "Express surprise when the nurse warns that your blister fluid can transmit chickenpox.",
            "Ask how long the blisters remain contagious to infants and pregnant women.",
            "Ask how to care for the rash at home without popping blisters or causing secondary infection.",
            "Agree to cancel babysitting until every blister has completely crusted over.",
        ],
    },
    47: {
        "description": "You are a 54-year-old sales executive suffering an excruciating attack of acute gout in your left big toe (9/10 pain) after barbecue ribs and beer. You cannot bear even a bedsheet touching your toe and want immediate relief.",
        "tasks": [
            "Beg the nurse not to touch your foot because the throbbing pain in your big toe is a 9/10.",
            "Describe how the agony flared up overnight following a feast of red meat and craft beer.",
            "Ask why dietary purines in beer, steaks, and shellfish trigger uric acid crystals in the joint.",
            "Ask how to take Colchicine and Naproxen safely without getting severe stomach upset.",
            "Ask why long-term preventive medication (Allopurinol) cannot be started during an acute flare.",
            "Agree to drink 2 to 3 litres of water daily, reduce beer consumption, and rest the elevated foot.",
        ],
    },
    48: {
        "description": "You are a 74-year-old patient in hospital isolation recovering from Clostridioides difficile diarrhea. You feel lonely and resentful about contact precautions, and you don't understand why staff insist on soap and water rather than alcohol hand sanitizer.",
        "tasks": [
            "Complain to the infection control nurse about feeling like an outcast in an isolation side room.",
            "Ask why hospital staff wear yellow gowns and gloves every time they enter your room.",
            "Ask why alcohol hand rub doesn't kill C. diff spores and why soap and water is required.",
            "Ask whether the hospital gave you this infection because your bed area was contaminated.",
            "Ask how many consecutive days of normal bowel movements are required before isolation ends.",
            "Agree to wash your hands with warm running water and soap every time you use the commode.",
        ],
    },
    49: {
        "description": "You are a 44-year-old woman on Day 1 after a total thyroidectomy. You have developed a bizarre tingling and prickling sensation around your lips and fingertips. You wonder if it is just a harmless lingering effect of the anesthetic.",
        "tasks": [
            "Mention the strange pins-and-needles sensation around your mouth and fingertips to the nurse.",
            "Describe how the tingling started an hour ago and is gradually spreading down your hands.",
            "Ask whether this numbness is an allergic reaction, a stroke, or lingering anesthesia.",
            "Allow the nurse to test for facial twitching (Chvostek's sign) and arm spasms (Trousseau's sign).",
            "Ask why surgical trauma can stun the parathyroid glands and cause blood calcium to drop.",
            "Cooperate with urgent blood testing and accept intravenous or oral calcium replacement therapy.",
        ],
    },
    50: {
        "description": "You are a 52-year-old heavy goods mechanic scheduled for hip replacement in 4 weeks. The surgeon warned that your operation will be cancelled unless you quit your 20-a-day cigarette habit. You are stressed and feel you cannot quit cold turkey.",
        "tasks": [
            "Complain to the pre-op nurse that the surgeon's smoking ultimatum is unfair and impossible.",
            "Explain that you have smoked a pack a day for 32 years and smoking is your main stress reliever.",
            "Ask why smoking matters so much if the surgeon is operating on your hip and not your lungs.",
            "Ask how carbon monoxide and nicotine double the risk of wound infection and joint loosening.",
            "Ask how combination nicotine replacement therapy (patches plus gum or inhalator) works.",
            "Accept a referral to the hospital stop-smoking service and set a quit date 4 weeks before surgery.",
        ],
    },
}


def build_final_scenarios():
    final_list = []
    for i, s in enumerate(OET_NURSING_SCENARIOS, 1):
        prof = PATIENT_PROFILES.get(i)
        old_content = s["content"]
        cand = old_content["candidate_card"]
        timings = old_content.get("timings", {"speaking_time": 300, "preparation_time": 180})
        setting = old_content.get("setting") or old_content.get("scenario", {}).get("setting", "General Clinic")

        new_scenario = {
            "title": s["title"],
            "question_type": "ROLE_PLAY",
            "difficulty": s["difficulty"],
            "duration": 480,
            "is_active": True,
            "content": {
                "setting": setting,
                "timings": {
                    "speaking_time": timings.get("speaking_time", 300),
                    "preparation_time": timings.get("preparation_time", 180),
                },
                "patient_card": {
                    "tasks": prof["tasks"],
                    "description": prof["description"],
                },
                "candidate_card": {
                    "role": "Nurse",
                    "tasks": cand["tasks"],
                    "description": cand["description"],
                },
            },
        }
        final_list.append(new_scenario)
    return final_list


if __name__ == "__main__":
    final_scenarios = build_final_scenarios()
    assert len(final_scenarios) == 50, f"Expected 50 scenarios, got {len(final_scenarios)}"

    output_code = '"""\nOfficial OET Nursing speaking role-play scenarios (50 complete cases).\nAll scenarios have Candidate role = Nurse and strictly adhere to the exact pattern:\n{\n  "setting": "...",\n  "timings": {"speaking_time": 300, "preparation_time": 180},\n  "patient_card": {"tasks": [...], "description": "..."},\n  "candidate_card": {"role": "Nurse", "tasks": [...], "description": "..."}\n}\n"""\n\n'
    output_code += "OET_NURSING_SCENARIOS = " + pprint.pformat(final_scenarios, indent=4, width=120) + "\n"

    with open("seeds/oet_nursing_scenarios.py", "w") as f:
        f.write(output_code)

    print("✅ Successfully built and wrote all 50 full OET Nursing scenarios to seeds/oet_nursing_scenarios.py!")
