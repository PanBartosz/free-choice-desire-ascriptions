import json
import os
import random
from collections import Counter, defaultdict

try:
    import pandas as pd
    HAS_PANDAS = True
except Exception:
    pd = None
    HAS_PANDAS = False


RNG_SEED = 42

NAMES = [
    "Alex", "Avery", "Bailey", "Blair", "Cameron", "Casey", "Charlie", "Corey",
    "Dakota", "Devin", "Drew", "Dylan", "Eden", "Elliot", "Emery", "Finley",
    "Frankie", "Harper", "Hayden", "Jamie", "Jordan", "Jules", "Kai", "Kendall",
    "Kennedy", "Lane", "Logan", "Marley", "Micah", "Morgan", "Parker", "Peyton",
    "Quinn", "Reese", "Remy", "Riley", "Robin", "Rowan", "Ryan", "Sage",
    "Sawyer", "Skyler", "Taylor", "Tegan", "Ari", "Kelly", "Leslie", "Shiloh",
]

BUNDLES = {
    "photography": [
        {"inf": "photograph the sculpture garden", "past": "photographed the sculpture garden", "ing": "photographing the sculpture garden"},
        {"inf": "edit the raw photos", "past": "edited the raw photos", "ing": "editing the raw photos"},
        {"inf": "set up the tripod", "past": "set up the tripod", "ing": "setting up the tripod"},
        {"inf": "charge the camera batteries", "past": "charged the camera batteries", "ing": "charging the camera batteries"},
        {"inf": "pack the lens kit", "past": "packed the lens kit", "ing": "packing the lens kit"},
        {"inf": "back up the memory cards", "past": "backed up the memory cards", "ing": "backing up the memory cards"},
        {"inf": "test the shutter remote", "past": "tested the shutter remote", "ing": "testing the shutter remote"},
        {"inf": "adjust the white balance", "past": "adjusted the white balance", "ing": "adjusting the white balance"},
        {"inf": "clean the camera sensor", "past": "cleaned the camera sensor", "ing": "cleaning the camera sensor"},
        {"inf": "scout the shooting location", "past": "scouted the shooting location", "ing": "scouting the shooting location"},
    ],
    "cooking": [
        {"inf": "chop the vegetables", "past": "chopped the vegetables", "ing": "chopping the vegetables"},
        {"inf": "boil the pasta", "past": "boiled the pasta", "ing": "boiling the pasta"},
        {"inf": "marinate the tofu", "past": "marinated the tofu", "ing": "marinating the tofu"},
        {"inf": "bake the rolls", "past": "baked the rolls", "ing": "baking the rolls"},
        {"inf": "simmer the sauce", "past": "simmered the sauce", "ing": "simmering the sauce"},
        {"inf": "preheat the oven", "past": "preheated the oven", "ing": "preheating the oven"},
        {"inf": "set the table", "past": "set the table", "ing": "setting the table"},
        {"inf": "grill the skewers", "past": "grilled the skewers", "ing": "grilling the skewers"},
        {"inf": "pack the leftovers", "past": "packed the leftovers", "ing": "packing the leftovers"},
        {"inf": "garnish the plates", "past": "garnished the plates", "ing": "garnishing the plates"},
    ],
    "maintenance": [
        {"inf": "paint the hallway", "past": "painted the hallway", "ing": "painting the hallway"},
        {"inf": "repair the loose hinge", "past": "repaired the loose hinge", "ing": "repairing the loose hinge"},
        {"inf": "tighten the cabinet screws", "past": "tightened the cabinet screws", "ing": "tightening the cabinet screws"},
        {"inf": "replace the lightbulb", "past": "replaced the lightbulb", "ing": "replacing the lightbulb"},
        {"inf": "clean the air filter", "past": "cleaned the air filter", "ing": "cleaning the air filter"},
        {"inf": "patch the wall crack", "past": "patched the wall crack", "ing": "patching the wall crack"},
        {"inf": "sweep the front porch", "past": "swept the front porch", "ing": "sweeping the front porch"},
        {"inf": "scrub the tile grout", "past": "scrubbed the tile grout", "ing": "scrubbing the tile grout"},
        {"inf": "organize the tool box", "past": "organized the tool box", "ing": "organizing the tool box"},
        {"inf": "test the smoke detector", "past": "tested the smoke detector", "ing": "testing the smoke detector"},
    ],
    "study": [
        {"inf": "read the article summary", "past": "read the article summary", "ing": "reading the article summary"},
        {"inf": "outline the report", "past": "outlined the report", "ing": "outlining the report"},
        {"inf": "edit the slide deck", "past": "edited the slide deck", "ing": "editing the slide deck"},
        {"inf": "print the handouts", "past": "printed the handouts", "ing": "printing the handouts"},
        {"inf": "review the survey data", "past": "reviewed the survey data", "ing": "reviewing the survey data"},
        {"inf": "draft the introduction", "past": "drafted the introduction", "ing": "drafting the introduction"},
        {"inf": "format the bibliography", "past": "formatted the bibliography", "ing": "formatting the bibliography"},
        {"inf": "annotate the source text", "past": "annotated the source text", "ing": "annotating the source text"},
        {"inf": "email the instructor questions", "past": "emailed the instructor questions", "ing": "emailing the instructor questions"},
        {"inf": "rehearse the presentation", "past": "rehearsed the presentation", "ing": "rehearsing the presentation"},
    ],
    "travel": [
        {"inf": "book the train tickets", "past": "booked the train tickets", "ing": "booking the train tickets"},
        {"inf": "confirm the hotel reservation", "past": "confirmed the hotel reservation", "ing": "confirming the hotel reservation"},
        {"inf": "pack the carry-on bag", "past": "packed the carry-on bag", "ing": "packing the carry-on bag"},
        {"inf": "renew the passport", "past": "renewed the passport", "ing": "renewing the passport"},
        {"inf": "check the boarding times", "past": "checked the boarding times", "ing": "checking the boarding times"},
        {"inf": "arrange the airport ride", "past": "arranged the airport ride", "ing": "arranging the airport ride"},
        {"inf": "print the travel itinerary", "past": "printed the travel itinerary", "ing": "printing the travel itinerary"},
        {"inf": "charge the power bank", "past": "charged the power bank", "ing": "charging the power bank"},
        {"inf": "download the maps", "past": "downloaded the maps", "ing": "downloading the maps"},
        {"inf": "set an early alarm", "past": "set an early alarm", "ing": "setting an early alarm"},
    ],
    "music": [
        {"inf": "tune the guitar", "past": "tuned the guitar", "ing": "tuning the guitar"},
        {"inf": "restring the instrument", "past": "restrung the instrument", "ing": "restringing the instrument"},
        {"inf": "practice the chorus", "past": "practiced the chorus", "ing": "practicing the chorus"},
        {"inf": "record a demo", "past": "recorded a demo", "ing": "recording a demo"},
        {"inf": "warm up the scales", "past": "warmed up the scales", "ing": "warming up the scales"},
        {"inf": "adjust the metronome", "past": "adjusted the metronome", "ing": "adjusting the metronome"},
        {"inf": "learn the bridge section", "past": "learned the bridge section", "ing": "learning the bridge section"},
        {"inf": "polish the lyrics", "past": "polished the lyrics", "ing": "polishing the lyrics"},
        {"inf": "mix the audio tracks", "past": "mixed the audio tracks", "ing": "mixing the audio tracks"},
        {"inf": "schedule a rehearsal", "past": "scheduled a rehearsal", "ing": "scheduling a rehearsal"},
    ],
    "gardening": [
        {"inf": "water the seedlings", "past": "watered the seedlings", "ing": "watering the seedlings"},
        {"inf": "trim the hedges", "past": "trimmed the hedges", "ing": "trimming the hedges"},
        {"inf": "plant the herb seeds", "past": "planted the herb seeds", "ing": "planting the herb seeds"},
        {"inf": "pull the weeds", "past": "pulled the weeds", "ing": "pulling the weeds"},
        {"inf": "rake the fallen leaves", "past": "raked the fallen leaves", "ing": "raking the fallen leaves"},
        {"inf": "stake the tomato vines", "past": "staked the tomato vines", "ing": "staking the tomato vines"},
        {"inf": "harvest the cucumbers", "past": "harvested the cucumbers", "ing": "harvesting the cucumbers"},
        {"inf": "compost the clippings", "past": "composted the clippings", "ing": "composting the clippings"},
        {"inf": "mulch the garden bed", "past": "mulched the garden bed", "ing": "mulching the garden bed"},
        {"inf": "clean the watering cans", "past": "cleaned the watering cans", "ing": "cleaning the watering cans"},
    ],
    "event_hosting": [
        {"inf": "arrange the seating", "past": "arranged the seating", "ing": "arranging the seating"},
        {"inf": "set up the projector", "past": "set up the projector", "ing": "setting up the projector"},
        {"inf": "test the microphone", "past": "tested the microphone", "ing": "testing the microphone"},
        {"inf": "prepare the snack table", "past": "prepared the snack table", "ing": "preparing the snack table"},
        {"inf": "label the name tags", "past": "labeled the name tags", "ing": "labeling the name tags"},
        {"inf": "greet the guests", "past": "greeted the guests", "ing": "greeting the guests"},
        {"inf": "collect the RSVPs", "past": "collected the RSVPs", "ing": "collecting the RSVPs"},
        {"inf": "review the agenda", "past": "reviewed the agenda", "ing": "reviewing the agenda"},
        {"inf": "cue the playlist", "past": "cued the playlist", "ing": "cueing the playlist"},
        {"inf": "dim the room lights", "past": "dimmed the room lights", "ing": "dimming the room lights"},
    ],
    "crafts": [
        {"inf": "sketch the layout", "past": "sketched the layout", "ing": "sketching the layout"},
        {"inf": "paint the background", "past": "painted the background", "ing": "painting the background"},
        {"inf": "cut the stencil", "past": "cut the stencil", "ing": "cutting the stencil"},
        {"inf": "glue the pieces", "past": "glued the pieces", "ing": "gluing the pieces"},
        {"inf": "sand the wooden edges", "past": "sanded the wooden edges", "ing": "sanding the wooden edges"},
        {"inf": "sew the fabric border", "past": "sewed the fabric border", "ing": "sewing the fabric border"},
        {"inf": "varnish the surface", "past": "varnished the surface", "ing": "varnishing the surface"},
        {"inf": "mount the canvas", "past": "mounted the canvas", "ing": "mounting the canvas"},
        {"inf": "frame the illustration", "past": "framed the illustration", "ing": "framing the illustration"},
        {"inf": "photograph the finished piece", "past": "photographed the finished piece", "ing": "photographing the finished piece"},
    ],
    "outdoors": [
        {"inf": "stretch the hamstrings", "past": "stretched the hamstrings", "ing": "stretching the hamstrings"},
        {"inf": "jog the trail loop", "past": "jogged the trail loop", "ing": "jogging the trail loop"},
        {"inf": "refill the water bottles", "past": "refilled the water bottles", "ing": "refilling the water bottles"},
        {"inf": "set up the yoga mats", "past": "set up the yoga mats", "ing": "setting up the yoga mats"},
        {"inf": "check the bike tires", "past": "checked the bike tires", "ing": "checking the bike tires"},
        {"inf": "pack the first-aid kit", "past": "packed the first-aid kit", "ing": "packing the first-aid kit"},
        {"inf": "map the running route", "past": "mapped the running route", "ing": "mapping the running route"},
        {"inf": "time the sprint intervals", "past": "timed the sprint intervals", "ing": "timing the sprint intervals"},
        {"inf": "cool down after practice", "past": "cooled down after practice", "ing": "cooling down after practice"},
        {"inf": "clean the exercise gear", "past": "cleaned the exercise gear", "ing": "cleaning the exercise gear"},
    ],
}


def format_text(template: str, name: str, action_a: dict, action_b: dict) -> str:
    fields = {
        "name": name,
        "A": action_a["inf"],
        "B": action_b["inf"],
        "A_past": action_a["past"],
        "B_past": action_b["past"],
        "A_ing": action_a["ing"],
        "B_ing": action_b["ing"],
    }
    return template.format(**fields)


# Each entry holds four varied skeletons per pair type.
CRITICAL_SPECS = [
    {
        "domain": "modal",
        "pair_type": "allowed_and",
        "valid": "?",
        "templates": [
            {"premise": "{name} is allowed to {A} or {B}.", "conclusion": "{name} is allowed to {A} and is allowed to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} has permission to {A} or to {B}.", "conclusion": "{name} has permission to {A} and has permission to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} is free to {A} or {B}.", "conclusion": "{name} is free to {A} and is free to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} is cleared to {A} or {B}.", "conclusion": "{name} is cleared to {A} and cleared to {B}.", "conclusion_form": "AND"},
        ],
    },
    {
        "domain": "modal",
        "pair_type": "allowed_single",
        "valid": "?",
        "templates": [
            {"premise": "{name} is allowed to {A} or {B}.", "conclusion": "{name} is allowed to {A}.", "conclusion_form": "A"},
            {"premise": "{name} has permission to {A} or to {B}.", "conclusion": "{name} has permission to {B}.", "conclusion_form": "B"},
            {"premise": "{name} is free to {A} or {B}.", "conclusion": "{name} is free to {A}.", "conclusion_form": "A"},
            {"premise": "{name} is cleared to {A} or {B}.", "conclusion": "{name} is cleared to {B}.", "conclusion_form": "B"},
        ],
    },
    {
        "domain": "modal",
        "pair_type": "must_and",
        "valid": "?",
        "templates": [
            {"premise": "{name} should {A} or {B}.", "conclusion": "{name} may {A}, and may {B}.", "conclusion_form": "AND"},
            {"premise": "{name} is supposed to {A} or {B}.", "conclusion": "{name} is allowed to {A} and is allowed to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} is expected to {A} or {B}.", "conclusion": "{name} is free to {A} and is free to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} is required to {A} or {B}.", "conclusion": "{name} is allowed to {A} and is allowed to {B}.", "conclusion_form": "AND"},
        ],
    },
    {
        "domain": "modal",
        "pair_type": "must_single",
        "valid": "?",
        "templates": [
            {"premise": "{name} should {A} or {B}.", "conclusion": "{name} may {A}.", "conclusion_form": "A"},
            {"premise": "{name} is supposed to {A} or {B}.", "conclusion": "{name} is allowed to {B}.", "conclusion_form": "B"},
            {"premise": "{name} is expected to {A} or {B}.", "conclusion": "{name} is allowed to  {A}.", "conclusion_form": "A"},
            {"premise": "{name} is required to {A} or {B}.", "conclusion": "{name} is free to {B}.", "conclusion_form": "B"},
        ],
    },
    {
        "domain": "modal",
        "pair_type": "all_and",
        "valid": "N",
        "templates": [
            {"premise": "Everyone {A_past} or {B_past}.", "conclusion": "Some people {A_past}, and some people {B_past}.", "conclusion_form": "AND"},
            {"premise": "Every participant {A_past} or {B_past}.", "conclusion": "At least one participant {A_past}, and at least one participant {B_past}.", "conclusion_form": "AND"},
            {"premise": "Each person {A_past} or {B_past}.", "conclusion": "At least one person {A_past}, and at least one  {B_past}.", "conclusion_form": "AND"},
            {"premise": "All of them {A_past} or {B_past}.", "conclusion": "Some of them  {A_past}, and some of them {B_past}.", "conclusion_form": "AND"},
        ],
    },
    {
        "domain": "modal",
        "pair_type": "all_single",
        "valid": "N",
        "templates": [
            {"premise": "Everyone {A_past} or {B_past}.", "conclusion": "Some people {A_past}.", "conclusion_form": "A"},
            {"premise": "Every participant {A_past} or {B_past}.", "conclusion": "At least one participant {B_past}.", "conclusion_form": "B"},
            {"premise": "Each person {A_past} or {B_past}.", "conclusion": "At least one person {A_past}.", "conclusion_form": "A"},
            {"premise": "All of them {A_past} or {B_past}.", "conclusion": "Some of them {B_past}.", "conclusion_form": "B"},
        ],
    },
    {
        "domain": "want",
        "pair_type": "want_and",
        "valid": "?",
        "templates": [
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {A} and wants to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {A} and wants to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {A} and wants to {B}.", "conclusion_form": "AND"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {A} and wants to {B}.", "conclusion_form": "AND"},
        ],
    },
    {
        "domain": "want",
        "pair_type": "want_single",
        "valid": "?",
        "templates": [
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {A}.", "conclusion_form": "A"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {B}.", "conclusion_form": "B"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {A}.", "conclusion_form": "A"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} wants to {B}.", "conclusion_form": "B"},
        ],
    },
    {
        "domain": "want",
        "pair_type": "want_mind_and",
        "valid": "?",
        "templates": [
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} does not mind {A_ing}, and does not mind {B_ing}.", "conclusion_form": "AND"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} is fine with {A_ing} and is fine with {B_ing}.", "conclusion_form": "AND"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} would be okay with {A_ing} and would be okay with {B_ing}.", "conclusion_form": "AND"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} has no objection to {A_ing} and has no objection to {B_ing}.", "conclusion_form": "AND"},
        ],
    },
    {
        "domain": "want",
        "pair_type": "want_mind_single",
        "valid": "?",
        "templates": [
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} does not mind {A_ing}.", "conclusion_form": "A"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} is fine with {B_ing}.", "conclusion_form": "B"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} would be okay with {A_ing}.", "conclusion_form": "A"},
            {"premise": "{name} wants to {A} or {B}.", "conclusion": "{name} has no objection to {B_ing}.", "conclusion_form": "B"},
        ],
    },
    {
        "domain": "want",
        "pair_type": "atleast_single_a",
        "valid": "?",
        "templates": [
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {A}.", "conclusion_form": "A"},
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {A}.", "conclusion_form": "A"},
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {A}.", "conclusion_form": "A"},
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {A}.", "conclusion_form": "A"},
        ],
    },
    {
        "domain": "want",
        "pair_type": "atleast_single_b",
        "valid": "?",
        "templates": [
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {B}.", "conclusion_form": "B"},
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {B}.", "conclusion_form": "B"},
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {B}.", "conclusion_form": "B"},
            {"premise": "{name} wants to {A} or at least {B}.", "conclusion": "{name} wants to {B}.", "conclusion_form": "B"},
        ],
    },
]


def build_action_pool(rng):
    pool = {}
    seen = set()
    for scenario, actions in BUNDLES.items():
        shuffled = [dict(a) for a in actions]
        rng.shuffle(shuffled)
        pool[scenario] = shuffled
        for action in shuffled:
            if action["inf"] in seen:
                raise ValueError(f"Duplicate action detected: {action['inf']}")
            if "ing" not in action:
                raise ValueError(f"Missing ing form for action: {action}")
            seen.add(action["inf"])
    total_actions = sum(len(v) for v in pool.values())
    if total_actions < 96:
        raise ValueError(f"Need at least 96 unique actions; found {total_actions}.")
    return pool


# Hand-crafted practice/control items grouped by category with 7 valid + 7 invalid.
HAND_ITEMS = {
    "conjunction": {
        "valid": [
            ("Sophia stopped by the bakery and bought fresh bread.", "Sophia went to the bakery."),
            ("Emma walked to the lake and fed the ducks.", "Emma gave food to the ducks."),
            ("Oliver called his brother and apologized for the argument.", "Oliver said he was sorry."),
            ("Jacob opened the window and let in some fresh air.", "Jacob allowed fresh air to enter the room."),
            ("The cyclist crossed the old bridge and took a break by the river.", "The cyclist rested near the water."),
            ("The student opened the window and aired out the room.", "The student let fresh air inside."),
            ("The drone circled over the field and recorded the migrating birds.", "The drone captured footage of the migrating birds."),
        ],
        "invalid": [
            ("The tourist visited the castle and photographed the courtyard.", "The tourist visited the cathedral."),
            ("Sophie cleaned the guest room and changed all the bed linens.", "Sophie attended a music festival."),
            ("Daniel organized the bookshelf and donated a stack of novels.", "Daniel had lunch at a sushi bar."),
            ("The delivery truck stopped at the warehouse and unloaded several crates.", "The delivery truck stopped at the supermarket."),
            ("The train passed through the village and slowed near the small station.", "The train ended its route in the village."),
            ("Liam repaired the old radio and tested its signal range.", "Liam travelled to the mountains."),
            ("Olivia watered the houseplants and trimmed the yellow leaves.", "Olivia met her colleagues for a late meeting."),
        ],
    },
    "conditional": {
        "valid": [
            ("Since heavy fog covered the valley, the hikers lost visibility.", "The hikers could no longer see their surroundings clearly."),
            ("Since the engine overheated, the car stopped on the roadside.", "The engine became too hot."),
            ("Since Maria forgot her umbrella, she got soaked on her way home.", "Maria didn’t take an umbrella with her."),
            ("Since the window remained open all night, the room became unusually cold.", "The room’s temperature dropped significantly."),
            ("Since Daniel overslept, he arrived at the meeting much later than planned.", "Daniel got up later than he intended."),
            ("Since Carla didn’t charge her phone, it died halfway through the call.", "Carla failed to charge her phone."),
            ("Since the electricity went out, the laboratory instruments shut down.", "The building lost electrical power."),
        ],
        "invalid": [
            ("If Laura finishes preparing the detailed report today, she will send it to the entire team.", "Laura will send the report to the team."),
            ("If the printer jams this morning, the reports will be delayed.", "The device will power off on its own."),
            ("If Adam visits the new exhibition, he will take some photos.", "Adam will go to see the new display."),
            ("If the software updates successfully, the interface will change.", "The layout will look different."),
            ("If the package arrives tomorrow, the office will process it immediately.", "The parcel will be handled in a week time."),
            ("If the lamp stops working, we will replace the bulb.", "The bulb will be changed."),
            ("If the door sensor malfunctions, the lights will stay on overnight.", "The lights will turn off early in the evening."),
        ],
    },
    "quantifier": {
        "valid": [
            ("Some blondes have dark eyes.", "Some people with dark eyes are blondes."),
            ("Some birds have long legs.", "Some creatures with long legs are birds."),
            ("Some cars have all-wheel drive.", "Some all-wheel-drive vehicles are cars."),
            ("All toads have poison glands.", "If you find a true toad in your garden, it will have poison glands."),
            ("Every table is a piece of furniture.", "If you have a table in your room, you have a piece of furniture."),
            ("There exists a book that has been read by everyone.", "Everyone read at least one book."),
            ("There is a person who is an idol for everyone.", "Everybody has an idol."),
        ],
        "invalid": [
            ("Some blondes have dark eyes.", "Some blondes have dark clothes."),
            ("Some birds have long legs.", "Some birds have long beaks."),
            ("Some cars have all-wheel drive.", "Some cars have dual exhaust."),
            ("All toads have poison glands.", "If you find a true toad in your garden, it may not have poison glands."),
            ("Every table is a piece of furniture.", "If you have only a table in your room, you don’t have any furniture."),
            ("Everyone read at least one book.", "There is a book that has been read by everyone."),
            ("Everybody has an idol.", "There is a person who is an idol for everyone."),
        ],
    },
    "presupposition": {
        "valid": [
            ("Alice won a car race.", "Alice participated in a car race."),
            ("John quit smoking last year.", "John used to smoke in the past."),
            ("Mary visited her brother.", "Mary has siblings."),
            ("Emma talked to her son.", "Emma has children."),
            ("Anne realized that the tire was flat.", "The tire was flat."),
            ("Ruth knows that roses require a lot of water.", "Roses need a lot of water."),
            ("Maggie spent holidays in Paris, again.", "Maggie had already visited Paris before."),
        ],
        "invalid": [
            ("Mark won a car race.", "Mark has never participated in a car race."),
            ("Anne quit smoking last year.", "Anne never smoked in the past."),
            ("Sue visited her brother.", "Sue has no siblings."),
            ("Andrew talked to his daughter.", "Andrew has two daughters."),
            ("Jim realized that the window was broken.", "Jim realized that there were two windows."),
            ("Albert knows that geraniums prefer full sun.", "Albert likes geraniums."),
            ("Thomas broke his leg, again.", "Thomas broke his arm in the past."),
        ],
    },
}


def build_critical_trials(canonical_only=False):
    rng = random.Random(RNG_SEED)
    names = NAMES.copy()
    rng.shuffle(names)
    name_iter = iter(names)

    actions_by_scenario = build_action_pool(rng)
    used_actions = set()
    single_types = {
        "allowed_single",
        "must_single",
        "all_single",
        "want_single",
        "want_mind_single",
        "atleast_single_a",
        "atleast_single_b",
    }
    balance_types = {
        "allowed_single",
        "must_single",
        "all_single",
        "want_single",
        "want_mind_single",
    }

    items = []
    for spec in CRITICAL_SPECS:
        if canonical_only:
            if spec["pair_type"] in single_types:
                # Alternate A/B forms using the canonical template, flipping roles for B.
                base = spec["templates"][0]
                if spec["pair_type"] in balance_types:
                    templates = []
                    for form in ["A", "B", "A", "B"]:
                        tcopy = dict(base)
                        tcopy["conclusion_form"] = form
                        tcopy["__flip__"] = form == "B"
                        templates.append(tcopy)
                else:
                    templates = [base] * 4
            else:
                templates = [spec["templates"][0]] * 4
        else:
            templates = spec["templates"]
        for tidx, template in enumerate(templates):
            try:
                name = next(name_iter)
            except StopIteration as exc:
                raise ValueError("Ran out of names while building critical trials.") from exc

            available = [s for s, acts in actions_by_scenario.items() if len(acts) >= 2]
            if not available:
                raise ValueError("Ran out of scenario actions while building critical trials.")
            scenario = rng.choice(available)
            actions = actions_by_scenario[scenario]
            action_a = actions.pop()
            action_b = actions.pop()

            if action_a["inf"] in used_actions or action_b["inf"] in used_actions:
                raise ValueError("Action reuse detected; pool must stay unique.")
            used_actions.add(action_a["inf"])
            used_actions.add(action_b["inf"])

            premise = format_text(template["premise"], name, action_a, action_b)
            conclusion_form = template["conclusion_form"]
            flip_roles = template.get("__flip__", False)
            if flip_roles:
                conclusion = format_text(template["conclusion"], name, action_b, action_a)
            else:
                conclusion = format_text(template["conclusion"], name, action_a, action_b)

            items.append({
                "PREMISE": premise,
                "CONCLUSION": conclusion,
                "DOMAIN": spec["domain"],
                "PAIR_TYPE": spec["pair_type"],
                "CONCLUSION_FORM": conclusion_form,
                "VALID": spec["valid"],
                "SCENARIO": scenario,
                "TEMPLATE_ID": 1 if canonical_only else tidx + 1,
                "ITEM": f"{spec['domain'][0].upper()}{len(items):02d}",
            })

    expected_actions = len(items) * 2
    if len(used_actions) != expected_actions:
        raise ValueError(f"Expected {expected_actions} unique action fillers, found {len(used_actions)}.")
    validate(items, canonical_only=canonical_only)
    return items


def validate(items, canonical_only=False):
    expected_items = 48
    if len(items) != expected_items:
        raise ValueError(f"Expected {expected_items} critical trials, found {len(items)}.")

    counts = Counter((it["DOMAIN"], it["PAIR_TYPE"]) for it in items)
    for spec in CRITICAL_SPECS:
        template_count = len(spec["templates"])
        expected = 4 if canonical_only else template_count
        key = (spec["domain"], spec["pair_type"])
        if counts[key] != expected:
            raise ValueError(f"Count mismatch for {key}: {counts[key]} vs {expected}")

    # Enforce A/B balance for single-conclusion variants.
    expected_balance = {
        "allowed_single": {"A": 2, "B": 2},
        "must_single": {"A": 2, "B": 2},
        "all_single": {"A": 2, "B": 2},
        "want_single": {"A": 2, "B": 2},
        "want_mind_single": {"A": 2, "B": 2},
        "atleast_single_a": {"A": 4, "B": 0},
        "atleast_single_b": {"A": 0, "B": 4},
    }
    forms_by_pair = defaultdict(Counter)
    for it in items:
        forms_by_pair[it["PAIR_TYPE"]][it["CONCLUSION_FORM"]] += 1
    for pair_type, expected_forms in expected_balance.items():
        for form, expected in expected_forms.items():
            actual = forms_by_pair[pair_type].get(form, 0)
            if actual != expected:
                raise ValueError(f"Unbalanced {pair_type}: expected {expected} {form} conclusions, found {actual}.")


def build_practice_and_controls():
    practice = []
    controls = []
    pid = 0
    cid = 0
    for category, sets in HAND_ITEMS.items():
        valid_items = sets["valid"]
        invalid_items = sets["invalid"]
        if len(valid_items) < 7 or len(invalid_items) < 7:
            raise ValueError(f"Need at least 7 valid and 7 invalid for category {category}.")

        def make_entry(prem, concl, valid_flag, item_id, kind):
            return {
                "PREMISE": prem,
                "CONCLUSION": concl,
                "DOMAIN": "control",
                "PAIR_TYPE": category,
                "CONCLUSION_FORM": "",
                "VALID": valid_flag,
                "ITEM": item_id,
                "SCENARIO": "",
                "TEMPLATE_ID": 0,
            }

        # First items for practice (one valid, one invalid)
        v_prem, v_concl = valid_items[0]
        practice.append(make_entry(v_prem, v_concl, "Y", f"P{pid:02d}", "practice"))
        pid += 1
        inv_prem, inv_concl = invalid_items[0]
        practice.append(make_entry(inv_prem, inv_concl, "N", f"P{pid:02d}", "practice"))
        pid += 1

        # Remaining 6 valid + 6 invalid become controls
        for prem, concl in valid_items[1:]:
            controls.append(make_entry(prem, concl, "Y", f"C{cid:02d}", "control"))
            cid += 1
        for prem, concl in invalid_items[1:]:
            controls.append(make_entry(prem, concl, "N", f"C{cid:02d}", "control"))
            cid += 1

    if len(practice) != 8:
        raise ValueError(f"Expected 8 practice items, found {len(practice)}.")
    if len(controls) != 48:
        raise ValueError(f"Expected 48 control items, found {len(controls)}.")
    return practice, controls


def write_js_var_json(items, path, varname):
    with open(path, 'w') as f:
        f.write(f"var {varname} = ")
        json.dump(items, f, indent=4)


def write_xlsx(items, path):
    if HAS_PANDAS:
        pd.DataFrame(items).to_excel(path, index=False)
    else:
        import csv
        keys = sorted({k for it in items for k in it.keys()})
        with open(path.replace('.xlsx', '.csv'), 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for it in items:
                writer.writerow(it)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate critical stimuli.")
    parser.add_argument("--canonical-only", action="store_true",
                        help="Use only the first (canonical) template per item type.")
    args = parser.parse_args()

    critical = build_critical_trials(canonical_only=args.canonical_only)
    practice, controls = build_practice_and_controls()
    experimental = critical + controls

    basedir = os.path.dirname(__file__)
    expdir = os.path.join(basedir, 'experiment')
    os.makedirs(expdir, exist_ok=True)

    write_js_var_json(experimental, os.path.join(expdir, 'stimuli_experimental.json'), 'stimuli_experimental')
    write_js_var_json(practice, os.path.join(expdir, 'stimuli_practice.json'), 'stimuli_practice')
    write_xlsx(experimental, os.path.join(basedir, 'stimuli_experimental.xlsx'))
    write_xlsx(practice, os.path.join(basedir, 'stimuli_practice.xlsx'))


if __name__ == '__main__':
    main()
