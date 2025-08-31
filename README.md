# Description of Data
Our data is on Pokemon. A more in depth explanation can be found at PokeAPI.co.
## Origin
This data was collected from PokeAPI.co. We wrote a script that requests data for each pokemon and collects the info we want in the appropriate format. The script is data_collection.py and can be ran
locally to create the data we have.
## Fields
### Boolean Fields
#### Legendary
The field 'legendary' represents whether or not the Pokemon is typically considered 'legendary'
#### Mythical
The field 'mythical' represents whether or not the Pokemon is typically considered 'mythical'
### Integer Fields
#### Attack
The field 'attack' represents the attack power of the Pokemon. This is used in battle.
#### Base Experience
The field 'base_experience' represents the amount of experience points gained by a Pokemon that knocks out this Pokemon, before modifiers are applied.
#### Capture Rate
The field 'capture_rate' represents how difficult the Pokemon is to capture. The maximum value is 255, representing the easiest to catch Pokemon.
#### Defense
The field 'defense' represents the defense power of the Pokemon. This is used in battle.
#### Gender Ratio
The field 'gender_ratio' represents the chance of an individual Pokemon of this species to be female. Since this is stored as an integer, it must be divided by eight to determine the actual percentage.
Some Pokemon species are genderless, in which case this field will be negative one.
#### Height
The field 'height' represents the height of the Pokemon in decimeters. Since decimeters aren't a standard form of measurement, the value should be divided by ten when displayed to show height in meters.
#### HP
The field 'hp' stands for health points and represents the health of the Pokemon. This is used in battle.
#### Number
The field 'number' represents the national Pokedex number of the Pokemon. It is mostly unique to it's Pokemon but some Pokemon have multiple 'forms' and thus have multiple entries each with the same
number.
#### Special Attack
The field 'special-attack' represents the attack power of the Pokemon for attacks classified as 'special.' This is used in battle.
#### Special Defense
The field 'special-defense' represents the defense power of the Pokemon for attacks classified as 'special.' This is used in battle.
#### Speed
The field 'speed' represents how fast the Pokemon is. This is used in battle.
#### Weight
The field 'weight' represents the weight of the Pokemon in hectograms. Just like height, the value should be divided by ten when displayed to show weight in kilograms.
### String Fields
#### Ability 1
The field 'ability1' represents the first ability a Pokemon may have. There are many possible values for this field, each corresponding to an in game effect.
#### Ability 2
The field 'ability2' represents the second ability a Pokemon may have. The possible values for this field are identical to 'ability1.' Every Pokemon has at least one possible ability, but may or may not
have two, therefore this field may not exist. An individual Pokemon can only have one ability. There is no distinction between the first and second ability.
#### Egg Group 1
The field 'egg_group1' represents the egg group a Pokemon is in. There are currently fifteen possible values for this field. This value is used to determine which other Pokemon a Pokemon can have
children with.
#### Egg Group 2
The field 'egg_group2' represents a possible second egg group a Pokemon is in. The values for this field are identical to 'egg_group1.' Not every Pokemon has a second egg group, this field may not exist.
There is no distinction between the first and second egg group.
#### Generation
The field 'generation' represents the generation the Pokemon was introduced. Nine generations of Pokemon have been released so far.
#### Growth Rate
The field 'growth_rate' represents how quickly a Pokemon gains experience. There are six possible values for this field, each of which correspond to a specific mathematical formula.
#### Hidden Ability
The field 'hidden_ability' represents the rare hidden ability a Pokemon may have. The possible values for this field are identical to 'ability1.' Not every Pokemon has a hidden ability, this field may
not exist.
#### Name
The field 'name' is the name of the Pokemon. It will be unique for each entry.
#### Type 1
The field 'type1' is the name of the primary type of the Pokemon. There are eighteen possible values for this field.
#### Type 2
The field 'type2' is the name of the secondary type of the Pokemon. The possible values for this field are identical to the possible values for 'type1.' Not all Pokemon have two types, this field may not
exist. For Pokemon with two types, while one type is technically 'primary' and one is technically 'secondary,' in practice this distinction doesn't affect anything and a Pokemon's two types are
interchangable.
