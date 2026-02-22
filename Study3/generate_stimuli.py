from collections import namedtuple
from random import shuffle
import random
import pandas as pd
import json
from collections import deque

Triplet = namedtuple("Triplet", ["Sweet", "Fruit", "Meat"])

sweets = ["a chocolate",
          "a cookie",
          "a biscuit",
          "a lollipop",
          "a cupcake",
          "a cake",
          "a muffin",
          "caramel",
          "a donut",
          "a brownie",
          ]

fruits = [
    "a strawberry",
    "a grapefruit",
    "a cranberry",
    "an apple",
    "a pear",
    "a cherry",
    "an orange",
    "a mango",
    "a plum",
    "a peach",
]

meats = [
    "a steak",
    "a burger",
    "a kebab",
    "a meatball",
    "a sausage",
    "a meatloaf",
    "a hotdog",
    "ribs",
    "pork",
    "beef",]

names = [
    # Male Names
    "James", "John", "Robert", "Michael", "William",
    "David", "Richard", "Joseph", "Thomas", "Charles",
    "Christopher", "Daniel", "Matthew", "Anthony", "Mark",
    "Donald", "Steven", "Paul", "Andrew", "Joshua",
    # Female Names
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth",
    "Barbara", "Susan", "Jessica", "Sarah", "Karen",
    "Nancy", "Lisa", "Margaret", "Betty", "Sandra",
    "Ashley", "Dorothy", "Kimberly", "Emily", "Donna"
]

random.Random(42).shuffle(names) # shuffling male/famale names

qs = []
for sweet, fruit, meat in zip(sweets, fruits, meats):
	qs.append(Triplet(Sweet=sweet, Fruit=fruit, Meat=meat))
qsr = deque(qs)
qsr.rotate(1)
qsr = list(qsr)

preferences = {
    "Urbanite": {"wants": "Sweet",
                  "accepts": "Meat",
                  "dislikes": "Fruit"},
    "Nomad": {"wants": "Fruit",
                  "accepts": "Meat",
                  "dislikes": "Sweet"},
}

def generate_experimental(q, firstname, region, verb, _type):
    item1 = q._asdict()[preferences[region][_type[0]]]
    item2 = q._asdict()[preferences[region][_type[1]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "wants to",
             "duration" : 500 
             },
            {"text" : "eat",
             "duration" : 250
             },
            {"text" : f"{item1} or {item2}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} wants to eat {item1} or {item2}",
		"VERB": verb,
		"CONDITION": "EXPERIMENTAL",
		"CORRECT": "Y/N",
        "TRIBE" : region,
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "ITEM2" : item2,
        "ITEM2_TYPE" : _type[1],
        }

def generate_experimental_mind(q, firstname, region, verb, _type, group = "all"):
    item1 = q._asdict()[preferences[region][_type[0]]]
    item2 = q._asdict()[preferences[region][_type[1]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "does not",
             "duration" : 500 
             },
            {"text" : "mind",
             "duration" : 250
             },
            {"text" : "eating",
             "duration" : 250
             },
            {"text" : f"{item1} or {item2}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} does not mind eating {item1} or {item2}",
		"VERB": verb,
		"CONDITION": "EXPERIMENTAL",
		"CORRECT": "Y/N",
        "TRIBE" : region,
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "ITEM2" : item2,
        "ITEM2_TYPE" : _type[1],
        "GROUP" : group
        }

def generate_single_control(q, firstname, region, verb, _type, group = "all"):
    item1 = q._asdict()[preferences[region][_type[0]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "wants to",
             "duration" : 500 
             },
            {"text" : "eat",
             "duration" : 250
             },
            {"text" : f"{item1}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} wants to eat {item1}",
		"VERB": verb,
		"CONDITION": "SINGLE_CONTROL",
		"CORRECT": "Y" if _type[0] == "wants" else "N",
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "GROUP" : group
        }

def generate_double_control(q1, q2, firstname, region, verb, _type, other, group = "all"):
    item1 = q1._asdict()[preferences[region][_type[0]]]
    item2 = q2._asdict()[preferences[region][other[0]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "wants to",
             "duration" : 500
             },
            {"text" : "eat",
             "duration" : 250 
             },
            {"text" : f"{item1} or {item2}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} wants to eat {item1} or {item2}",
		"VERB": verb,
		"CONDITION": "DOUBLE_CONTROL",
		"CORRECT": "Y" if other[0] == "wants" else "N",
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "ITEM2" : item2,
        "ITEM1_TYPE" : other[0],
        "GROUP" : group
        }


def generate_single_control_fine(q, firstname, region, verb, _type, group = "all"):
    item1 = q._asdict()[preferences[region][_type[0]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "is fine",
             "duration" : 500 
             },
            {"text" : "with",
             "duration" : 250
             },
            {"text" : "eating",
             "duration" : 250
             },
            {"text" : f"{item1}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} is fine with eating {item1}",
		"VERB": verb,
		"CONDITION": "SINGLE_CONTROL_FINE",
		"CORRECT": "Y" if _type[0] in ["wants", "accepts"] else "N",
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "GROUP" : group
        }

def generate_double_control_fine(q1, q2, firstname, region, verb, _type, other, group = "all"):
    item1 = q1._asdict()[preferences[region][_type[0]]]
    item2 = q2._asdict()[preferences[region][other[0]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "is fine",
             "duration" : 500 
             },
            {"text" : "with",
             "duration" : 250
             },
            {"text" : "eating",
             "duration" : 250
             },
            {"text" : f"{item1} or {item2}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} is fine with eating {item1} or {item2}",
		"VERB": verb,
		"CONDITION": "DOUBLE_CONTROL_FINE",
		"CORRECT": "Y" if (other[0] in ["wants", "accepts"]) and (_type[0] in ["wants", "accepts"]) else "N", # TODO: to chyba nie jest prawda
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "ITEM2" : item2,
        "ITEM1_TYPE" : other[0],
        "GROUP" : group
        }

def generate_single_control_mind(q, firstname, region, verb, _type, group = "all"):
    item1 = q._asdict()[preferences[region][_type[0]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "does not",
             "duration" : 500 
             },
            {"text" : "mind",
             "duration" : 250
             },
            {"text" : "eating",
             "duration" : 250
             },
            {"text" : f"{item1}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} does not mind eating {item1}",
		"VERB": verb,
		"CONDITION": "SINGLE_CONTROL_MIND",
		"CORRECT": "Y" if _type[0] in ["wants", "accepts"] else "N",
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "GROUP" : group
        }

def generate_double_control_mind(q1, q2, firstname, region, verb, _type, other, group = "all"):
    item1 = q1._asdict()[preferences[region][_type[0]]]
    item2 = q2._asdict()[preferences[region][other[0]]]
    return {
        "SEGMENTS" : [
            {"text" : f"{firstname}-the-{region}",
             "duration" : 750
             },
            {"text" : "does not",
             "duration" : 500 
             },
            {"text" : "mind",
             "duration" : 250
             },
            {"text" : "eating",
             "duration" : 250
             },
            {"text" : f"{item1} or {item2}",
             },
        ],
        "SENTENCE" : f"{firstname}-the-{region} is does not mind eating {item1} or {item2}",
		"VERB": verb,
		"CONDITION": "DOUBLE_CONTROL_MIND",
		"CORRECT": "Y" if (other[0] in ["wants", "accepts"]) and (_type[0] in ["wants", "accepts"]) else "N", # TODO: to chyba nie jest prawda
        "ITEM1" : item1,
        "ITEM1_TYPE" : _type[0],
        "ITEM2" : item2,
        "ITEM1_TYPE" : other[0],
        "GROUP" : group
        }

# Generate experimental positions

N_EXPERIMENTAL = 5
N_DOUBLE_CONTROL = 5
N_SINGLE_CONTROL = 5

items = []

######################
# EXPERIMENTAL ITEMS #
######################
i_counter = 0
for j in range(N_EXPERIMENTAL):
	item = generate_experimental(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type=["wants", "dislikes"] if i_counter % 2 == 0 else [
                           "dislikes", "wants"]
    )

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_experimental(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type=["wants", "accepts"] if i_counter % 2 == 0 else [
                           "accepts", "wants"]
    )

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_experimental(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type=["accepts", "dislikes"] if i_counter % 2 == 0 else [
                           "dislikes", "accepts"]
    )

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1


for j in range(N_EXPERIMENTAL, N_EXPERIMENTAL * 2):
	item = generate_experimental(qs[j], names[i_counter],
                        region="Nomad",
                        verb="want",
                       _type=["wants", "dislikes"] if i_counter % 2 == 0 else [
                           "dislikes", "wants"]
    )
	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_experimental(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type=["wants", "accepts"] if i_counter % 2 == 0 else [
                           "accepts", "wants"]
    )

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_experimental(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type=["accepts", "dislikes"] if i_counter % 2 == 0 else [
                           "dislikes", "accepts"]
    )

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1


##################################################################
i_counter = 0
for j in range(N_DOUBLE_CONTROL):
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="want",
                                _type = ["wants"],
                                other= ["wants"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1


	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="want",
                                _type = ["dislikes"],
                                other= ["dislikes"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="want",
                                _type = ["accepts"],
                                other= ["accepts"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(N_DOUBLE_CONTROL, N_DOUBLE_CONTROL*2):
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="want",
                                _type = ["wants"],
                                other= ["wants"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1


	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="want",
                                _type = ["dislikes"],
                                other= ["dislikes"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="want",
                                _type = ["accepts"],
                                other= ["accepts"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

i_counter = 0
for j in range(N_SINGLE_CONTROL):
	item = generate_single_control(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type = ["wants"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type = ["dislikes"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type = ["accepts"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(N_SINGLE_CONTROL, N_SINGLE_CONTROL*2):
	item = generate_single_control(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type = ["wants"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type = ["dislikes"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type = ["accepts"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1



## Additional stimuli (12 in total)

names_add = [
    "Ryan", "Kevin", "Brian", "George", "Nathan", "Justin",
    "Amanda", "Michelle", "Laura", "Melissa", "Stephanie", "Rebecca"
]

random.Random(42).shuffle(names_add) # shuffling male/famale names

qs_add = []
for sweet, fruit, meat in zip(['a popsicle', "a marshmallow", "a truffle", "a candy"],
                              ['a blueberry', "a pineapple", "a papaya", "an apricot"],
                              ['chicken', "a ham", "bacon", "a roast"]):
	qs_add.append(Triplet(Sweet=sweet, Fruit=fruit, Meat=meat))


i_counter = 30 
for j in range(2):
	item = generate_single_control(qs_add[j], names_add[i_counter-30],
                       region="Urbanite",
                       verb="want",
                       _type = ["wants"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs_add[j], names_add[i_counter-30],
                       region="Urbanite",
                       verb="want",
                       _type = ["dislikes"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs_add[j], names_add[i_counter-30],
                       region="Urbanite",
                       verb="want",
                       _type = ["accepts"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(2, 4):
	item = generate_single_control(qs_add[j], names_add[i_counter-30],
                       region="Nomad",
                       verb="want",
                       _type = ["wants"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs_add[j], names_add[i_counter-30],
                       region="Nomad",
                       verb="want",
                       _type = ["dislikes"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

	item = generate_single_control(qs_add[j], names_add[i_counter-30],
                       region="Nomad",
                       verb="want",
                       _type = ["accepts"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1



# Additional _mind stimuli  (8 items – 4 doublets) 

sweets_mind = ['gingerbread', 'pudding', 'fudge', 'an eclair', 'a sorbet', 'a strudel', 'a crepe', 'nougat']
fruits_mind = ['a banana', 'a kiwi', 'a pomegranate', 'a raspberry', 'a lychee','a nectarine','a dragonfruit', 'a clementine']
meats_mind  = ['turkey', 'salami', 'lamb', 'duck', 'brisket', 'veal', 'pastrami', 'mutton']

names_mind = [
    "Adam", "Ethan", "Benjamin", "Kyle", "Olivia", "Grace",
    "Hannah", "Chloe", "Dylan", "Ian", "Julia", "Sophie",
    'Aaron','Brooke','Cameron','Delilah','Edward','Fiona',
    'Gabriel','Hailey','Isla','Jonah','Kara','Logan', 
    "Quentin","Victor", "Wesley","Xavier","Yvonne","Zoe",
    "Lily","Madison","Nora",
]

assert not (set(sweets_mind) & (set(sweets) | {t.Sweet for t in qs_add}))
assert not (set(fruits_mind) & (set(fruits) | {t.Fruit for t in qs_add}))
assert not (set(meats_mind)  & (set(meats)  | {t.Meat  for t in qs_add}))
assert not (set(names_mind)  & (set(names)  | set(names_add)))

random.Random(42).shuffle(names_mind)
qs_mind = [Triplet(s, f, m)
           for s, f, m in zip(sweets_mind, fruits_mind, meats_mind)]
i_counter = 42

for j in range(2):
    # URBANITE + MIND + D
	item = generate_single_control_mind(qs_mind[j], names_mind[i_counter-42],
                       region="Urbanite",
                       verb="does not mind",
                       _type = ["dislikes"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"M{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + MIND + A
	item = generate_single_control_mind(qs_mind[j], names_mind[i_counter-42],
                       region="Urbanite",
                       verb="does not mind",
                       _type = ["accepts"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"M{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(2, 4):
    # NOMAD + MIND + D
	item = generate_single_control_mind(qs_mind[j], names_mind[i_counter-42],
                       region="Nomad",
                       verb="does not mind",
                       _type = ["dislikes"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"M{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + MIND + A
	item = generate_single_control_mind(qs_mind[j], names_mind[i_counter-42],
                       region="Nomad",
                       verb="does not mind",
                       _type = ["accepts"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"M{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(4, 6):
    # URBANITE + MIND + D/D
	item = generate_double_control_mind(qs_mind[j], qsr[j],
                                names_mind[i_counter-42],
                                region="Urbanite",
                                verb="does not mind",
                                _type = ["dislikes"],
                                other= ["dislikes"])
	item["ITEM"] = f"N{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + MIND + A/A
	item = generate_double_control_mind(qs_mind[j], qsr[j],
                                names_mind[i_counter-42],
                                region="Urbanite",
                                verb="does not mind",
                                _type = ["accepts"],
                                other= ["accepts"])
	item["ITEM"] = f"N{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(6, 8):

    # NOMAD + MIND + D/D
	item = generate_double_control_mind(qs_mind[j], qsr[j],
                                names_mind[i_counter-42],
                                region="Nomad",
                                verb="does not mind",
                                _type = ["dislikes"],
                                other= ["dislikes"])
	item["ITEM"] = f"N{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + MIND + A/A
	item = generate_double_control_mind(qs_mind[j], qsr[j],
                                names_mind[i_counter-42],
                                region="Nomad",
                                verb="does not mind",
                                _type = ["accepts"],
                                other= ["accepts"])
	item["ITEM"] = f"N{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(2):
    # URBANITE + MIND + W/D 
	# item = generate_experimental_mind(qs_mind[j], names_mind[i_counter-58],
    #                    region="Urbanite",
    #                    verb="does not mind",
    #                    _type=["wants", "dislikes"] if i_counter % 2 == 0 else [
    #                        "dislikes", "wants"],
    #                    group = "mind"
    # )
	# item["ITEM"] = f"Z{i_counter}"
	# items.append(item)
	# i_counter += 1

    # # URBANITE + MIND + W/A 
	# item = generate_experimental_mind(qs_mind[j], names_mind[i_counter-58],
    #                    region="Urbanite",
    #                    verb="does not mind",
    #                    _type=["wants", "accepts"] if i_counter % 2 == 0 else [
    #                        "accepts", "wants"],
    #                    group = "mind"
    # )
	# item["ITEM"] = f"Z{i_counter}"
	# items.append(item)
	# i_counter += 1

    # URBANITE + MIND + D/A 
	item = generate_experimental_mind(qs_mind[j], names_mind[i_counter-58],
                       region="Urbanite",
                       verb="does not mind",
                       _type=["dislikes", "accepts"] if i_counter % 2 == 0 else [
                           "accepts", "dislikes"],
                       group = "mind"
    )
	item["ITEM"] = f"Z{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(2, 4):
    # NOMAD + MIND + W/D 
	# item = generate_experimental_mind(qs_mind[j], names_mind[i_counter-58],
    #                    region="Nomad",
    #                    verb="does not mind",
    #                    _type=["wants", "dislikes"] if i_counter % 2 == 0 else [
    #                        "dislikes", "wants"],
    #                    group = "mind"
    # )
	# item["ITEM"] = f"Z{i_counter}"
	# items.append(item)
	# i_counter += 1

    # # NOMAD + MIND + W/A 
	# item = generate_experimental_mind(qs_mind[j], names_mind[i_counter-58],
    #                    region="Nomad",
    #                    verb="does not mind",
    #                    _type=["wants", "accepts"] if i_counter % 2 == 0 else [
    #                        "accepts", "wants"],
    #                    group = "mind"
    # )
	# item["ITEM"] = f"Z{i_counter}"
	# items.append(item)
	# i_counter += 1

    # NOMAD + MIND + D/A 
	item = generate_experimental_mind(qs_mind[j], names_mind[i_counter-58],
                       region="Nomad",
                       verb="does not mind",
                       _type=["dislikes", "accepts"] if i_counter % 2 == 0 else [
                           "accepts", "dislikes"],
                       group = "mind"
    )
	item["ITEM"] = f"Z{i_counter}"
	items.append(item)
	i_counter += 1



pd.DataFrame(items).to_excel("stimuli_experimental.xlsx")
with open("stimuli_experimental.json", "w") as f:
    json.dump(items, f, indent=4)



# Practice session
N_TRAINING = 2
items = []

i_counter = 0
for j in range(N_TRAINING):
    # URBANITE + W
	item = generate_single_control(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type = ["wants"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + D
	item = generate_single_control(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type = ["dislikes"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + A
	item = generate_single_control(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="want",
                       _type = ["accepts"],
                       group = "meat"
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + MIND + D
	item = generate_single_control_mind(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="does not mind",
                       _type = ["dislikes"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"F{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + MIND + A
	item = generate_single_control_mind(qs[j], names[i_counter],
                       region="Urbanite",
                       verb="does not mind",
                       _type = ["accepts"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"F{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(N_TRAINING, N_TRAINING*2):
    # NOMAD + W
	item = generate_single_control(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type = ["wants"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + D
	item = generate_single_control(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type = ["dislikes"]
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

    # Nomad + A
	item = generate_single_control(qs[j], names[i_counter],
                       region="Nomad",
                       verb="want",
                       _type = ["accepts"],
                       group = "meat"
    )
                       
	item["ITEM"] = f"S{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + MIND + D
	item = generate_single_control_mind(qs[j], names[i_counter],
                       region="Nomad",
                       verb="does not mind",
                       _type = ["dislikes"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"F{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + MIND + A
	item = generate_single_control_mind(qs[j], names[i_counter],
                       region="Nomad",
                       verb="does not mind",
                       _type = ["accepts"],
                       group = "mind"
    )
                       
	item["ITEM"] = f"F{i_counter}"
	items.append(item)
	i_counter += 1

i_counter = 0
for j in range(N_TRAINING):
    # NOMAD + W/W
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="want",
                                _type = ["wants"],
                                other= ["wants"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + D/D
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="want",
                                _type = ["dislikes"],
                                other= ["dislikes"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + A/A
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="want",
                                _type = ["accepts"],
                                other= ["accepts"],
                                group = "meat")

	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + MIND + A/A
	item = generate_double_control_mind(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="does not mind",
                                _type = ["accepts"],
                                other= ["accepts"],
                                group = "mind")

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + MIND + D/D
	item = generate_double_control_mind(qs[j], qsr[j],
                                names[i_counter],
                                region="Nomad",
                                verb="does not mind",
                                _type = ["dislikes"],
                                other= ["dislikes"],
                                group = "mind")

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

for j in range(N_TRAINING, N_TRAINING*2):
    # URBANITE + W/W
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="want",
                                _type = ["wants"],
                                other= ["wants"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + D/D
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="want",
                                _type = ["dislikes"],
                                other= ["dislikes"])
	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + A/A
	item = generate_double_control(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="want",
                                _type = ["accepts"],
                                other= ["accepts"],
                                group = "meat")

	item["ITEM"] = f"D{i_counter}"
	items.append(item)
	i_counter += 1

    # URBANITE + MIND + A/A
	item = generate_double_control_mind(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="does not mind",
                                _type = ["accepts"],
                                other= ["accepts"],
                                group = "mind")

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

    # NOMAD + MIND + D/D
	item = generate_double_control_mind(qs[j], qsr[j],
                                names[i_counter],
                                region="Urbanite",
                                verb="does not mind",
                                _type = ["dislikes"],
                                other= ["dislikes"],
                                group = "mind")

	item["ITEM"] = f"E{i_counter}"
	items.append(item)
	i_counter += 1

pd.DataFrame(items).to_excel("stimuli_practice.xlsx")
with open("stimuli_practice.json", "w") as f:
    json.dump(items, f, indent=4)
