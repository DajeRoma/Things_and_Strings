# -*- coding: utf-8 -*-

import csv
import codecs
import sys
import nltk.data
from nltk.tokenize import WordPunctTokenizer, word_tokenize
import codecs


reload(sys)  
sys.setdefaultencoding('utf8')


"""
In Python 2,
	str: binary data (raw 8-bit values), e.g., accii and utf-8
	unicode: Unicode characters
* Operate on raw 8-bit values that are UTF-8-encoded (or other encoding)
* Operate on Unicode characters that have no specific encoding
"""
def to_unicode(unicode_or_str):
	if isinstance(unicode_or_str, str):
		value = unicode_or_str.decode('utf-8')
	else:
		value = unicode_or_str
	return value


def to_str(unicode_or_str):
	if isinstance(unicode_or_str, unicode):
		value = unicode_or_str.encode('utf-8')
	else:
		value = unicode_or_str
	return value


def write_listOfList_to_CSV(listOfList, csv_file_path):
	with open(csv_file_path, 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for listEntry in listOfList:
			spamwriter.writerow(listEntry)


def read_listOfList_from_CSV(csv_file_path):
	listOfList = []
	with open(csv_file_path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
		for row in spamreader:
			listOfList.append(row)
	return listOfList


def write_listOfStrings_to_txt(listOfStrings, txt_file_path):
	with codecs.open(txt_file_path, 'w', encoding='utf8') as outfile:
		for string in listOfStrings:
			string = string.decode('utf-8', errors='replace').encode('utf-8')
			outfile.write(string + '\n')


def read_from_txt_to_str(txt_file_path):
	with codecs.open(txt_file_path, 'rb', encoding='utf8') as outfile:
		line_list = outfile.readlines()
	line_list = [line.strip() for line in line_list]
	print len(line_list)
	return "\n".join(line_list).strip()



"""
	Given a string, tokenize the string into a list of sentences
		Punkt Sentence Tokenizer
"""
def tokenize_to_sents(text):
	sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
	sents = [sent.strip() for sent in sent_detector.tokenize(text.strip())]
	return sents


"""
	Given a string, tokenize the string (a sentence) into a list of words
		Punkt Word Tokenizer
"""
def tokenize_sent_to_words(sent):
	return word_tokenize(sent)


"""
	Given a string, tokenize the string (one or multiple sentences) into 
	  a list of sentences first and then to words
		Punkt Sentence Tokenizer + Punkt Word Tokenizer
"""
def tokenized_to_words(text):
	words = []
	text = codecs.utf_8_decode(text.encode('utf8'))
	text = text[0]
	for sent in tokenize_to_sents(text):
		words.extend(tokenize_sent_to_words(sent))
	return words



if __name__ == "__main__":
	sent1 = """
Washington, D.C., formally the District of Columbia and commonly referred to as "Washington", "the District", or simply "D.C.", is the capital of the United States.
The signing of the Residence Act on July 16, 1790, approved the creation of a capital district located along the Potomac River on the country's East Coast.
The U.S. Constitution provided for a federal district under the exclusive jurisdiction of the Congress and the District is therefore not a part of any state.
The states of Maryland and Virginia each donated land to form the federal district, which included the pre-existing settlements of Georgetown and Alexandria.
Named in honor of President George Washington, the City of Washington was founded in 1791 to serve as the new national capital.
In 1846, Congress returned the land originally ceded by Virginia; in 1871, it created a single municipal government for the remaining portion of the District.
Washington had an estimated population of 681,170 as of July 2016.
Commuters from the surrounding Maryland and Virginia suburbs raise the city's population to more than one million during the workweek.
The Washington metropolitan area, of which the District is a part, has a population of over 6 million, the sixth-largest metropolitan statistical area in the country.
The centers of all three branches of the federal government of the United States are in the District, including the Congress, President, and Supreme Court.
Washington is home to many national monuments and museums, which are primarily situated on or around the National Mall.
The city hosts 176 foreign embassies as well as the headquarters of many international organizations, trade unions, non-profit organizations, lobbying groups, and professional associations.
A locally elected mayor and a 13‑member council have governed the District since 1973.
However, the Congress maintains supreme authority over the city and may overturn local laws.
D.C. residents elect a non-voting, at-large congressional delegate to the House of Representatives, but the District has no representation in the Senate.
The District receives three electoral votes in presidential elections as permitted by the Twenty-third Amendment to the United States Constitution, ratified in 1961.
Various tribes of the Algonquian-speaking Piscataway people (also known as the Conoy) inhabited the lands around the Potomac River when Europeans first visited the area in the early 17th century.
One group known as the Nacotchtank (also called the Nacostines by Catholic missionaries) maintained settlements around the Anacostia River within the present-day District of Columbia.
Conflicts with European colonists and neighboring tribes forced the relocation of the Piscataway people, some of whom established a new settlement in 1699 near Point of Rocks, Maryland.
"""
	sent2 = """
Milford is a coastal city in southwestern New Haven County, Connecticut, United States, located between Bridgeport and New Haven.
The population was 52,759 at the 2010 census.
The city contains the incorporated borough of Woodmont and the unincorporated village of Devon.
The land which today comprises Milford, Orange and West Haven was purchased on February 1, 1639 from Ansantawae, chief of the local Paugussets (an Algonquian tribe) by English settlers affiliated with the contemporary New Haven Colony.
Originally, the area was known as "Wepawaug", after the small river which runs through the town, and which has given its name to several streets in both Milford and Orange.
A grist mill was first built over the Wepawaug River in 1640.
During the Revolutionary War the Milford section of the Boston Post Road, a vital route connecting Boston, New York and other major coastal cities, was blockaded by Continental forces, and Fort Trumbull was constructed to protect the town.
The site of the blockade is commemorated by the Liberty Rock monument.
By 1822, the town had grown large enough that residents in the northern and eastern sections of Milford chartered their own independent course as the town of Orange.
During the next century and a half, the remaining section of Milford was known for shipbuilding, farming and oystering, although a small subset of industrial facilities also developed in town. During this time, Milford also became known as a beach resort for residents of New Haven and Bridgeport.
Interestingly, the boundaries of the final town charter granted by the State of Connecticut in 1899 to Laurel Beach are contained entirely within Milford. Residents of Laurel Beach must therefore pay taxes to both Laurel Beach as well as Milford, and all mail to Laurel Beach residents is mailed to Milford.
Also in 1899, the "Memorial Bridge" (a "stone bridge and tower commemorating the town's history and founders") was built at the site of the last mill over the Wepawaug after it was closed in 1894.
"The stone bridge is simple in design, its broad copings surmounted with rough hewn blocks of granite, bearing the names of the first settlers.
There are ten blocks on the south and twenty on the north coping.
At each end of the former is a stone four feet wide by five and a half high."
It is located where Broad Street crosses the Wepawaug River.
In 1903, the southeastern portion of the town was incorporated as the Borough of Woodmont. In 1959, the town of Milford including the Borough of Woodmont was incorporated as the City of Milford.
Milford was one of the early settlements in south central Connecticut and, over time, gave rise to several new towns that broke off and incorporated separately.
The following is a list of towns created from parts of Milford.
Woodbridge in 1784 (also partly from New Haven)
Bethany, created from Woodbridge in 1832
Orange (originally North Milford) in 1822 (also partly from New Haven)
West Haven, created from Orange in 1921
Starting in 1902, Quaker Oats oatmeal boxes came with a coupon redeemable for the legal deed to a tiny lot in Milford.
The lots, sometimes as small as 10 feet (3 m) by 10 feet, were carved out of a 15-acre (6.1 ha) tract in a never-built subdivision called "Liberty Park".
A small number of children (or their parents), often residents living near Milford, collected the deeds and started paying the extremely small property taxes on the "oatmeal lots".
The developer of the prospective subdivision hoped the landowners would hire him to build homes on the lots, although several lots would need to be combined before building could start.
Since the subdivision into small lots predated Milford's planning and zoning regulations, the deeds were entirely legal, although they created a large amount of paperwork for town tax collectors, who frequently couldn't find the property owners and received almost no tax revenue from the lots.
In the mid-1970s, when the town wanted to develop the area, town officials put an end to the oatmeal lots in a "general foreclosure" that avoided the enormous expense of individual foreclosures by condemning nearly all of the property in one legal filing.
One of the streets in the Liberty Park subdivision plans, Shelland Street, was later built in the late 1990s as an access road to the Milford Power Company.
The site is currently home to the BIC Corporation's lighter factory at 565 Bic Drive.
(In a separate land giveaway in 1955 tied to the Sergeant Preston of the Yukon television show, Quaker Oats offered in its Puffed Wheat and Puffed Rice cereal boxes genuine deeds to land in the Klondike.)
Post-World War II development
In the post-World War II period, Milford—like many Connecticut towns—underwent significant suburbanization. Interstate 95 was routed through town, and the Milford section was completed in 1958.
The 1960s and 1970s witnessed the construction of the Connecticut Post Mall, one of the state's largest shopping malls, and the extensive commercial development of the town's stretch of the Boston Post Road. One notable small business located on the Boston Post Road during the 1970s was SCELBI Computer Consulting, credited by many as being the world's first personal-computer manufacturer. Starting in 1975, the city began hosting the Milford Oyster Festival, which has since become firmly established as an annual Milford tradition that is held "rain or shine".
The city became host to several headquarters of multinational corporations, including the Schick Shaving company, and Doctor's Associates, Inc., owners of the Subway chain of fast-food restaurants.
The US operations of BIC were headquartered in Milford, but in March 2008 moved most of its operations to Shelton.
Milford Hospital has also developed into an important health care resource for the area.
It has also become home of smaller national corporations such as K-Mart and Orchid Medical.
Government
Government in the city is set up with the mayor as chief executive and the Board of Aldermen as a legislative body.
The mayor is permitted to propose legislation to the Board of Aldermen and introduces the city budget, but possesses no veto power over what the Aldermen chooses to pass.
Taxes
In 2005, the mill rate for Milford was 34.36 and is 27.88 mills for fiscal year 2015–2016.
Elected positions
The following is a list of city government positions elected by city residents and the terms thereof:
Mayor: The mayor is the city's chief executive and is elected in odd-numbered years.
The mayor receives compensation for his or her services.
Board of Aldermen: The Board of Aldermen consists of 15 members elected in odd-numbered years, three from each of the city's five political districts.
Per City Charter requirements, only two of the three aldermen elected from each district may be from one political party to allow for minority representation on the board; voters are permitted to vote for any three aldermen in their district.
Members of the Board of Aldermen receive no compensation for their services.
Board of Education: The Board of Education deals with educational matters in the city and consists of 10 members elected in odd-numbered years, two from each of the city's five political districts. Members receive no compensation for their services.
Planning & Zoning Board: The Planning & Zoning Board deals with development and land use issues and consists of 10 members, two from each of the city's five political districts.
Members serve a four-year term, with one of the two members of each political district up for election during each odd-numbered year's election cycle, ensuring that no more than half of the board is made up of new members at the start of a new session.
Members of the Planning & Zoning Board receive no compensation for their services.
City Clerk: The city clerk is elected in odd-numbered years and receives a compensation for services provided.
Constables: Seven constables are elected in odd-numbered years, though individual voters are only permitted to vote for any four of their choosing on the ballot. They are compensated on a case-by-case basis.
Registrars of Voters: Pursuant to Connecticut state law, each town must have a Republican and Democratic registrar of voters to serve as election administrators, though an additional third party registrar is permitted if they receive more votes than either of the major parties' registrar.
Registrars in Milford are elected to two-year terms, their election taking place during each even-year state election cycle. Registrars are compensated for their services. Voters may only vote for one choice for registrar.
List of mayors
After becoming incorporated as a city in 1959, the city reformed its system of government by establishing a mayor–board of aldermen format.
It elected its first mayor, Charles Iovino, the incumbent city manager under Milford's previous form of government, on November 3, 1959.
Since 1959, 10 people have held the office of mayor in the city.
Education
Milford public schools currently operates eight Elementary schools, three Middle schools, two High schools, and one Alternative Education High school.
There are also a number of private schools in the city.
High Schools
Joseph A. Foran High School
Jonathan Law High School
The Academy 
Middle Schools
Harborside Middle School
East Shore Middle School
West Shore Middle School
Elementary Schools
John F. Kennedy Elementary School 
Pumpkin Delight Elementary School 
Mathewson Elementary School 
Meadowside Elementary School 
Orange Avenue Elementary School 
Calf Pen Meadow Elementary School 
Live Oaks Elementary School 
Orchard Hills Elementary School 
Technical Schools
Platt Technical High School
Private Schools
Academy of Our Lady of Mercy, Lauralton Hall High School
Milford Christian Academy (K-12)
Connecticut Center for Child Development (K-12)
The Foundation School (9-12)
Charles F. Hayden School (K-8) 
St. Mary School (PK-8)
Former Schools
Milford High School (closed 1983)
Simon Lake Elementary School (closed 2010)
St. Ann School (closed 2010)
St. Gabriel School (closed 2016)
Central Grammar School
Point Beach School
Fannie Beach School
Seabreeze School
Lenox Avenue School
West Main Street School
Fort Trumbull school
Fire Department
The city of Milford is protected 24/7, 365 by the 114 paid, full-time firefighters of the city of Milford Fire Department - ISO Class 1. The Milford Fire Department currently operates out of five fire stations, located throughout the city, under the command of a Battalion Chief and a Shift Commander.
The Milford Fire Department also maintains and operates a fire apparatus fleet of seven engines (including two Quints), one tower ladder, two rescue ambulances, one HazMat unit, one dive rescue unit, one collapse rescue unit, two fireboats, a canteen unit, and numerous other special, support, and reserve units.
The Milford Fire Department is one of only two fire departments in the state of Connecticut to maintain an ISO Class 1 rating. The current Fire Chief is Douglas Edo.
Fire station locations and apparatus
Below is a complete listing of all fire station locations and apparatus in the city of Milford.
The Milford Fire Department also operates four reserve engines. Engine 2 (Reserve) is located at the quarters of Engine 1 and Tower 1.
Engines 8 and 10 (Reserve) are located at the quarters of Engine 3 (Quint) and Engine 4, while Engine 9 (Reserve) is located at the quarters of Engine's 5 and 6. The Canteen Unit is operated out of a garage at 3 Charles Street.
Police department
The Milford Police Department is led by Chief Keith L. Mello, a 1981 graduate of the town's police academy. On May 12, 2011, the Police Officer Standards & Training Council re-accredited the department's Tier I & II State Accreditation.
Principal communities of Milford
Downtown Milford
Devon
Rivercliff
Morningside
Point Beach
Bayview
Walnut Beach
Wildermere Beach
Laurel Beach
Borough of Woodmont
Other minor communities and geographic features are Anchor Beach, Bayview Heights, Burwells Beach, Cedar Beach, Downtown Historic District, Ettadore Park, Far View Beach, Forest Heights, Fort Trumbull, Great River, Gulf Beach, Laurel Beach, Lexington Green, Merwin's Beach, Merwin's Point, Milford Lawns, Milford Point, Myrtle Beach, Naugatuck Gardens, Point Lookout, Silver Sands Beach, South of the Green, Walnut Beach, Wheelers Farms.
†denotes that the community is chartered by Special Act of the Connecticut General Assembly and have been granted some of the powers normally held only by a municipality including taxing authority. ‡The Borough of Woodmont is chartered by Special Act of the Connecticut General Assembly as a municipality and has been granted all statutory powers of an municipality while simultaneously remaining part of the city of Milford.
Culture
Every year on the third Saturday in August, Milford celebrates its annual Oyster Festival, which serves as a combination of a typical town fair with a culinary celebration of the town's location on historically shellfish-rich Long Island Sound. This festival takes place in and around the Milford Green, near the center of town, as well as in various locations throughout the downtown area, and features a wide variety of events including canoe and kayak races, musical performances, and classic car shows.
The Milford Oyster Festival has drawn large musical acts over the years including Joan Jett, The Marshall Tucker Band, John Cafferty & The Beaver Brown Band, Soul Asylum, and many more.
There are also other features such as carnival rides, food stands, crafts, face painting, and even opening your own oyster for a pearl.
The Milford Cultural Center, operated by the Milford Council for the Arts, offers various events throughout the year. The Firehouse Art Gallery was recently opened in Devon. The beach resort quality of the town lives on, with several rocky beaches, Silver Sands State Park, the Connecticut Audubon Society Coastal Center at Milford Point, Charles Island, two golf courses, and numerous other recreational facilities available for residents and tourists.
Starting in 2011, the Walnut Beach Concert Series has taken place under the pavilion at Walnut Beach. It features a different band playing every Sunday afternoon during the summer.
Top employers
According to the City's 2013 Comprehensive Annual Financial Report, the top employers in the city are:
According to the United States Census Bureau, Milford, including the borough of Woodmont, has a total area of 26.1 square miles (67.7 km2), of which 22.2 square miles (57.4 km2) is land and 3.9 square miles (10.2 km2), or 15.11%, is water.
Milford's Devon neighborhood is located at the mouth of the Housatonic River near Stratford, and features the Connecticut Audubon Coastal Center overlooking the estuary.
Islands and coastline
Milford has over 14 miles (23 km) of shoreline facing Long Island Sound, the most of any town in Connecticut. A large portion of Milford's shoreline forms the Silver Sands State Park. A newly built 3/4 mile boardwalk was opened in 2011 that connects Silver Sands to Walnut Beach in Devon. Charles Island is also a part of the park and is a protected bird nesting ground. There is a sand bar (called a tombolo since it is perpendicular, not parallel to the coast) accessible during low tide that people can walk on from Silver Sands Beach to Charles Island.
The island is a part of the Hamonasset-Ledyard Moraine and was formed as glaciers retreated at the end of the last ice age. The Wisconsin glaciation formed drumlins in Milford: Clark, Burwell, Eels, Bryan and Merwin hills.
Milford owns three islands in the Housatonic River: Fowler Island, just to the south of the Igor I. Sikorsky Memorial Bridge, Duck Island, and Nells Island, both near the mouth of the river. In addition to Silver Sands State Park, Milford has five public beaches with lifeguard services for its residents - Gulf Beach, Anchor Beach, Hawley Avenue Beach, Walnut Beach, and Middle Beach - as well as seven private beaches.
Interstate 95 and U.S. Route 1 pass through the southern part of Milford. The Wilbur Cross Parkway cuts across the northern part of the city and is connected to I-95 and Route 1 via the Milford Parkway, also known as the Daniel S. Wasson connector, named for the first police officer to die in the line of duty in the city of Milford. He was killed on April 12, 1987, when he was shot by a motorist he had pulled over. The Metro-North New Haven Line has a station stop in downtown Milford (Milford station). The Milford Transit District provides in-town service to major attractions. Connections with the Greater Bridgeport Transit Authority and Connecticut Transit New Haven are also available.
As of the census of 2000, there were 52,212 people, 20,138 households, and 13,613 families residing in Milford. The population density was 2,270.7 people per square mile (876.8/km2). There were 21,145 housing units at an average density of 949.0 per square mile (366.4/km2). The racial makeup of Milford was 93.55% White, 1.91% African American, 0.13% Native American, 2.36% Asian, 0.03% Pacific Islander, 0.88% from other races, and 1.14% from two or more races. Hispanic or Latino of any race were 3.34% of the population.
There were 20,138 households out of which 29.3% had children under the age of 18 living with them, 54.7% were married couples living together, 9.7% had a female householder with no husband present, and 32.4% were non-families. 26.3% of all households were made up of individuals and 10.3% had someone living alone who was 65 years of age or older. The average household size was 2.49 and the average family size was 3.04.
In Milford the population was spread out with 22.4% under the age of 18, 5.9% from 18 to 24, 31.7% from 25 to 44, 25.0% from 45 to 64, and 14.9% who were 65 years of age or older. The median age was 39 years. For every 100 females there were 93.6 males. For every 100 females age 18 and over, there were 90.0 males.
As of the 2000 census, the median income for a household was $61,183. The per capita income was $28,773. About 2.4% of families and 3.8% of the population were below the poverty line, including 4.1% of those under age 18 and 5.4% of those age 65 or over.
The Census Bureau's 2010–2012 American Community Survey showed that (in 2012 inflation-adjusted dollars) median household income was $77,925 and the median family income was $93,697. Year-round male workers had a median income of $67,631 versus $59,992 for females. The per capita income for the city was $38,560.
Academy of Our Lady of Mercy Lauralton Hall — 200 High St. (added in 2011)
Buckingham House — 61 North St. (added in 1977)
Eells-Stow House — 34 High St. (added in 1977)
Hebrew Congregation of Woodmont — 15 and 17 Edgefield Ave. (added in 1995)
Housatonic River Railroad Bridge — Amtrak right-of-way at Housatonic River (added in 1987)
Milford Point Hotel — Milford Point Road (added in 1988)
River Park Historic District — Roughly bounded by Boston Post Road, Cherry St. and Amtrak, and High St. (added in 1986)
St. Peter's Episcopal Church — 61, 71, 81 River St. (added in 1979)
Taylor Memorial Library — 5 Broad St. (added in 1979)
US Post Office-Milford Main — 6 W. River St. (added in 1986)
Washington Bridge — Spans the Housatonic River to Stratford (added in 2004)
Dan Patrick, NBC's Football Night in America co-host, senior writer for Sports Illustrated, and former ESPN SportsCenter anchor
John Ratzenberger, actor
Justin Gallagher, famous bike jump builder
Dylan Bruno, actor
Anne Griffin, actress
Doug Henry, National Champion motocross & snowmobile racer
Simon Lake (1866–1945), inventor and naval engineer
Jonathan Law (1674–1750), colonial era judge, Governor of the Colony of Connecticut between 1741 and 1750
Joseph Plumb Martin (1760–1850), Revolutionary War soldier, raised by his grandparents in Milford
Abigail Merwin (1759–1786), colonial-era wife and mother who alerted the local militia of a raid by British forces arriving from the warship HMS Swan
Ellen Muth, actress
Erin Pac, 2010 women’s bobsled Olympic bronze medalist
Jason Peter, Collegiate All-American defensive tackle (1997) & defensive end for the Carolina Panthers, attended Milford Academy
Catherine Pollard (c. 1918–2006), first female Scoutmaster in the Boy Scouts of America
Charles H. Pond (1781–1861), judge of the New Haven County Court, sheriff of New Haven, Lieutenant Governor & 37th Governor of Connecticut
Peter Pond (1739/40?–1807), first explorer of the Athabasca region of North America in the 1780s & founding member of the North West Company
Peter L. Pond (1933–2000), human rights activist and philanthropist who adopted 16 Cambodian orphans
Jonathan Quick, NHL goaltender for the Los Angeles Kings, Stanley Cup champion
Christy Carlson Romano, actress
Dan Rusanowsky, NHL radio broadcaster for the San Jose Sharks
Al Scaduto (1928–2007), cartoonist (They'll Do It Every Time)
Frank J. Sprague (1857–1934), inventor who helped develop the electric motor, electric railways, and electric elevators
Robert Treat (c. 1624–1710), colonial era deputy & military officer, Governor of the Colony of Connecticut between 1683 and 1698
Jeff Davis, creator of the TV show Teen Wolf
Mark Arcobello, former NHL forward, who tied a league record for most teams played on during a single season.
Mary Kate Malat, actress/commercial model
Movies filmed at least in part in Milford include:
The Light That Failed (1916) - Smith's Point was used in a desert battle scene using camels from Barnum's circus in Bridgeport.
Man on a Swing (1974)
Daylight (1996)
Furious Fish (2005)
Save the Forest (2005)
December Plans (2007)
Righteous Kill (2008)
Sad Sack Sally (2009)
A Dance for Grace (2010)
This Wretched Life (2010)
After The Fall (2013)
Anything It Takes (2016)
City of Milford official website
Milford Historical Society
Downtown Milford Business Association
Milford's HamletHub, Milford's Local Stories
Milford, Connecticut at DMOZ
"Early Milford", history of Milford
Milford Living magazine
1646 map of Milford
MilfordRadio.com, community information
"""

	sent3 = """
Washington, D.C., formally the District of Columbia and commonly referred to as "Washington", "the District", or simply "D.C.", is the capital of the United States.
The signing of the Residence Act on July 16, 1790, approved the creation of a capital district located along the Potomac River on the country's East Coast.
The U.S. Constitution provided for a federal district under the exclusive jurisdiction of the Congress and the District is therefore not a part of any state.
The states of Maryland and Virginia each donated land to form the federal district, which included the pre-existing settlements of Georgetown and Alexandria.
Named in honor of President George Washington, the City of Washington was founded in 1791 to serve as the new national capital.
In 1846, Congress returned the land originally ceded by Virginia; in 1871, it created a single municipal government for the remaining portion of the District.
Washington had an estimated population of 681,170 as of July 2016.
Commuters from the surrounding Maryland and Virginia suburbs raise the city's population to more than one million during the workweek.
The Washington metropolitan area, of which the District is a part, has a population of over 6 million, the sixth-largest metropolitan statistical area in the country.
The centers of all three branches of the federal government of the United States are in the District, including the Congress, President, and Supreme Court.
Washington is home to many national monuments and museums, which are primarily situated on or around the National Mall.
The city hosts 176 foreign embassies as well as the headquarters of many international organizations, trade unions, non-profit organizations, lobbying groups, and professional associations.
A locally elected mayor and a 13‑member council have governed the District since 1973.
However, the Congress maintains supreme authority over the city and may overturn local laws.
D.C. residents elect a non-voting, at-large congressional delegate to the House of Representatives, but the District has no representation in the Senate.
The District receives three electoral votes in presidential elections as permitted by the Twenty-third Amendment to the United States Constitution, ratified in 1961.
Various tribes of the Algonquian-speaking Piscataway people (also known as the Conoy) inhabited the lands around the Potomac River when Europeans first visited the area in the early 17th century.
One group known as the Nacotchtank (also called the Nacostines by Catholic missionaries) maintained settlements around the Anacostia River within the present-day District of Columbia.
Conflicts with European colonists and neighboring tribes forced the relocation of the Piscataway people, some of whom established a new settlement in 1699 near Point of Rocks, Maryland.
In his Federalist No.
43, published January 23, 1788, James Madison argued that the new federal government would need authority over a national capital to provide for its own maintenance and safety.
Five years earlier, a band of unpaid soldiers besieged Congress while its members were meeting in Philadelphia.
Known as the Pennsylvania Mutiny of 1783, the event emphasized the need for the national government not to rely on any state for its own security.
Article One, Section Eight, of the Constitution permits the establishment of a "District (not exceeding ten miles square) as may, by cession of particular states, and the acceptance of Congress, become the seat of the government of the United States".
However, the Constitution does not specify a location for the capital.
In what is now known as the Compromise of 1790, Madison, Alexander Hamilton, and Thomas Jefferson came to an agreement that the federal government would pay each state's remaining Revolutionary War debts in exchange for establishing the new national capital in the Southern United States.
Foundation
On July 9, 1790, Congress passed the Residence Act, which approved the creation of a national capital on the Potomac River.
The exact location was to be selected by President George Washington, who signed the bill into law on July 16.
Formed from land donated by the states of Maryland and Virginia, the initial shape of the federal district was a square measuring 10 miles (16 km) on each side, totaling 100 square miles (259 km2).
Two pre-existing settlements were included in the territory: the port of Georgetown, Maryland, founded in 1751, and the city of Alexandria, Virginia, founded in 1749.
During 1791–92, Andrew Ellicott and several assistants, including a free African American astronomer named Benjamin Banneker, surveyed the borders of the federal district and placed boundary stones at every mile point.
Many of the stones are still standing.
A new federal city was then constructed on the north bank of the Potomac, to the east of Georgetown.
On September 9, 1791, the three commissioners overseeing the capital's construction named the city in honor of President Washington.
The federal district was named Columbia, which was a poetic name for the United States commonly in use at that time.
Congress held its first session in Washington on November 17, 1800.
Congress passed the Organic Act of 1801, which officially organized the District and placed the entire territory under the exclusive control of the federal government.
Further, the unincorporated area within the District was organized into two counties: the County of Washington to the east of the Potomac and the County of Alexandria to the west.
After the passage of this Act, citizens living in the District were no longer considered residents of Maryland or Virginia, which therefore ended their representation in Congress.
On August 24–25, 1814, in a raid known as the Burning of Washington, British forces invaded the capital during the War of 1812.
The Capitol, Treasury, and White House were burned and gutted during the attack.
Most government buildings were repaired quickly; however, the Capitol was largely under construction at the time and was not completed in its current form until 1868.
Retrocession and the Civil War
In the 1830s, the District's southern territory of Alexandria went into economic decline partly due to neglect by Congress.
The city of Alexandria was a major market in the American slave trade, and pro-slavery residents feared that abolitionists in Congress would end slavery in the District, further depressing the economy.
Alexandria's citizens petitioned Virginia to take back the land it had donated to form the District, through a process known as retrocession.
The Virginia General Assembly voted in February 1846 to accept the return of Alexandria and on July 9, 1846, Congress agreed to return all the territory that had been ceded by Virginia.
Therefore, the District's current area consists only of the portion originally donated by Maryland.
Confirming the fears of pro-slavery Alexandrians, the Compromise of 1850 outlawed the slave trade in the District, although not slavery itself.
The outbreak of the American Civil War in 1861 led to expansion of the federal government and notable growth in the District's population, including a large influx of freed slaves.
President Abraham Lincoln signed the Compensated Emancipation Act in 1862, which ended slavery in the District of Columbia and freed about 3,100 enslaved persons, nine months prior to the Emancipation Proclamation.
In 1868, Congress granted the District's African American male residents the right to vote in municipal elections.
Growth and redevelopment
By 1870, the District's population had grown 75% from the previous census to nearly 132,000 residents.
Despite the city's growth, Washington still had dirt roads and lacked basic sanitation.
Some members of Congress suggested moving the capital further west, but President Ulysses S. Grant refused to consider such a proposal.
Congress passed the Organic Act of 1871, which repealed the individual charters of the cities of Washington and Georgetown, and created a new territorial government for the whole District of Columbia.
President Grant appointed Alexander Robey Shepherd to the position of governor in 1873.
Shepherd authorized large-scale projects that greatly modernized Washington, but ultimately bankrupted the District government.
In 1874, Congress replaced the territorial government with an appointed three-member Board of Commissioners.
The city's first motorized streetcars began service in 1888 and generated growth in areas of the District beyond the City of Washington's original boundaries.
Washington's urban plan was expanded throughout the District in the following decades.
Georgetown was formally annexed by the City of Washington in 1895.
However, the city had poor housing conditions and strained public works.
Washington was the first city in the nation to undergo urban renewal projects as part of the "City Beautiful movement" in the early 1900s.
Increased federal spending as a result of the New Deal in the 1930s led to the construction of new government buildings, memorials, and museums in Washington.
World War II further increased government activity, adding to the number of federal employees in the capital; by 1950, the District's population reached its peak of 802,178 residents.
Civil rights and home rule era
The Twenty-third Amendment to the United States Constitution was ratified in 1961, granting the District three votes in the Electoral College for the election of president and vice president, but still no voting representation in Congress.
After the assassination of civil rights leader Dr. Martin Luther King, Jr., on April 4, 1968, riots broke out in the District, primarily in the U Street, 14th Street, 7th Street, and H Street corridors, centers of black residential and commercial areas.
The riots raged for three days until more than 13,600 federal troops stopped the violence.
Many stores and other buildings were burned; rebuilding was not completed until the late 1990s.
In 1973, Congress enacted the District of Columbia Home Rule Act, providing for an elected mayor and 13-member council for the District.
In 1975, Walter Washington became the first elected and first black mayor of the District.
On September 11, 2001, terrorists hijacked American Airlines Flight 77 and deliberately crashed the plane into the Pentagon in nearby Arlington, Virginia.
United Airlines Flight 93, believed to be destined for Washington, D.C., crashed in Pennsylvania when passengers tried to recover control of the plane from hijackers.
Washington, D.C., is located in the mid-Atlantic region of the U.S. East Coast.
Due to the District of Columbia retrocession, the city has a total area of 68.34 square miles (177.0 km2), of which 61.05 square miles (158.1 km2) is land and 7.29 square miles (18.9 km2) (10.67%) is water.
The District is bordered by Montgomery County, Maryland, to the northwest; Prince George's County, Maryland, to the east; and Arlington and Alexandria, Virginia, to the south and west.
The south bank of the Potomac River forms the District's border with Virginia and has two major tributaries: the Anacostia River and Rock Creek.
Tiber Creek, a natural watercourse that once passed through the National Mall, was fully enclosed underground during the 1870s.
The creek also formed a portion of the now-filled Washington City Canal, which allowed passage through the city to the Anacostia River from 1815 until the 1850s.
The Chesapeake and Ohio Canal starts in Georgetown and was used during the 19th century to bypass the Little Falls of the Potomac River, located at the northwest edge of Washington at the Atlantic Seaboard fall line.
The highest natural elevation in the District is 409 feet (125 m) above sea level at Fort Reno Park in upper northwest Washington.
The lowest point is sea level at the Potomac River.
The geographic center of Washington is near the intersection of 4th and L Streets NW.
Contrary to the urban legend, Washington was not built on a reclaimed swamp, but wetlands did cover areas along the water.
The District has 7,464 acres (30.21 km2) of parkland, about 19% of the city's total area and the second-highest percentage among high-density U.S. cities.
The National Park Service manages most of the 9,122 acres (36.92 km2) of city land owned by the U.S. government.
Rock Creek Park is a 1,754-acre (7.10 km2) urban forest in Northwest Washington, which extends 9.3 miles (15.0 km) through a stream valley that bisects the city.
Established in 1890, it is the country's fourth-oldest national park and is home to a variety of plant and animal species including raccoon, deer, owls, and coyotes.
Other National Park Service properties include the C&O Canal National Historical Park, the National Mall and Memorial Parks, Theodore Roosevelt Island, Columbia Island, Fort Dupont Park, Meridian Hill Park, Kenilworth Park and Aquatic Gardens, and Anacostia Park.
The D.C. Department of Parks and Recreation maintains the city's 900 acres (3.6 km2) of athletic fields and playgrounds, 40 swimming pools, and 68 recreation centers.
The U.S. Department of Agriculture operates the 446-acre (1.80 km2) U.S. National Arboretum in Northeast Washington.
Climate
Washington is in the northern part of the humid subtropical climate zone (Köppen: Cfa) However, under the Trewartha climate classification, the city has a temperate maritime climate (Do).
Winters are usually chilly with light snow, and summers are hot and humid.
The District is in plant hardiness zone 8a near downtown, and zone 7b elsewhere in the city, indicating a humid subtropical climate.
Spring and fall are mild to warm, while winter is chilly with annual snowfall averaging 15.5 inches (39 cm).
Winter temperatures average around 38 °F (3.3 °C) from mid-December to mid-February.
Summers are hot and humid with a July daily average of 79.8 °F (26.6 °C) and average daily relative humidity around 66%, which can cause moderate personal discomfort.
The combination of heat and humidity in the summer brings very frequent thunderstorms, some of which occasionally produce tornadoes in the area.
Blizzards affect Washington on average once every four to six years.
The most violent storms are called "nor'easters", which often affect large sections of the East Coast.
From January 27 to 28, 1922, the city officially received 28 inches (71 cm) of snowfall, the largest snowstorm since official measurements began in 1885.
According to notes kept at the time, the city received between 30 and 36 inches (76 and 91 cm) from a snowstorm on January 1772.
Hurricanes (or their remnants) occasionally track through the area in late summer and early fall, but are often weak by the time they reach Washington, partly due to the city's inland location.
Flooding of the Potomac River, however, caused by a combination of high tide, storm surge, and runoff, has been known to cause extensive property damage in the neighborhood of Georgetown.
Precipitation occurs throughout the year.
The highest recorded temperature was 106 °F (41 °C) on August 6, 1918, and on July 20, 1930. while the lowest recorded temperature was −15 °F (−26 °C) on February 11, 1899, during the Great Blizzard of 1899.
During a typical year, the city averages about 37 days at or above 90 °F (32.2 °C) and 64 nights at or below freezing.
Washington, D.C., is a planned city.
In 1791, President Washington commissioned Pierre (Peter) Charles L'Enfant, a French-born architect and city planner, to design the new capital.
He enlisted Scottish surveyor Alexander Ralston helped layout the city plan.
The L'Enfant Plan featured broad streets and avenues radiating out from rectangles, providing room for open space and landscaping.
He based his design on plans of cities such as Paris, Amsterdam, Karlsruhe, and Milan that Thomas Jefferson had sent to him.
L'Enfant's design also envisioned a garden-lined "grand avenue" approximately 1 mile (1.6 km) in length and 400 feet (120 m) wide in the area that is now the National Mall.
President Washington dismissed L'Enfant in March 1792 due to conflicts with the three commissioners appointed to supervise the capital's construction.
Andrew Ellicott, who had worked with L'Enfant surveying the city, was then tasked with completing the design.
Though Ellicott made revisions to the original plans, including changes to some street patterns, L'Enfant is still credited with the overall design of the city.
By the early 1900s, L'Enfant's vision of a grand national capital had become marred by slums and randomly placed buildings, including a railroad station on the National Mall.
Congress formed a special committee charged with beautifying Washington's ceremonial core.
What became known as the McMillan Plan was finalized in 1901 and included re-landscaping the Capitol grounds and the National Mall, clearing slums, and establishing a new citywide park system.
The plan is thought to have largely preserved L'Enfant's intended design.
By law, Washington's skyline is low and sprawling.
The federal Heights of Buildings Act of 1910 allows buildings that are no taller than the width of the adjacent street, plus 20 feet (6.1 m).
Despite popular belief, no law has ever limited buildings to the height of the United States Capitol or the 555-foot (169 m) Washington Monument, which remains the District's tallest structure.
City leaders have criticized the height restriction as a primary reason why the District has limited affordable housing and traffic problems caused by urban sprawl.
The District is divided into four quadrants of unequal area: Northwest (NW), Northeast (NE), Southeast (SE), and Southwest (SW).
The axes bounding the quadrants radiate from the U.S. Capitol building.
All road names include the quadrant abbreviation to indicate their location and house numbers generally correspond with the number of blocks away from the Capitol.
Most streets are set out in a grid pattern with east–west streets named with letters (e.g., C Street SW), north–south streets with numbers (e.g., 4th Street NW), and diagonal avenues, many of which are named after states.
The City of Washington was bordered by Boundary Street to the north (renamed Florida Avenue in 1890), Rock Creek to the west, and the Anacostia River to the east.
Washington's street grid was extended, where possible, throughout the District starting in 1888.
Georgetown's streets were renamed in 1895.
Some streets are particularly noteworthy, such as Pennsylvania Avenue, which connects the White House to the Capitol and K Street, which houses the offices of many lobbying groups.
Washington hosts 177 foreign embassies, constituting approximately 297 buildings beyond the more than 1,600 residential properties owned by foreign countries, many of which are on a section of Massachusetts Avenue informally known as Embassy Row.
Architecture
The architecture of Washington varies greatly.
Six of the top 10 buildings in the American Institute of Architects' 2007 ranking of "America's Favorite Architecture" are in the District of Columbia: the White House; the Washington National Cathedral; the Thomas Jefferson Memorial; the United States Capitol; the Lincoln Memorial; and the Vietnam Veterans Memorial.
The neoclassical, Georgian, gothic, and modern architectural styles are all reflected among those six structures and many other prominent edifices in Washington.
Notable exceptions include buildings constructed in the French Second Empire style such as the Eisenhower Executive Office Building.
Outside downtown Washington, architectural styles are even more varied.
Historic buildings are designed primarily in the Queen Anne, Châteauesque, Richardsonian Romanesque, Georgian revival, Beaux-Arts, and a variety of Victorian styles.
Rowhouses are especially prominent in areas developed after the Civil War and typically follow Federalist and late Victorian designs.
Georgetown's Old Stone House was built in 1765, making it the oldest-standing original building in the city.
Founded in 1789, Georgetown University features a mix of Romanesque and Gothic Revival architecture.
The Ronald Reagan Building is the largest building in the District with a total area of approximately 3.1 million square feet (288,000 m2).
The U.S. Census Bureau estimates that the District's population was 681,170 on July 1, 2016, an 13.2% increase since the 2010 United States Census.
The increase continues a growth trend since 2000, following a half-century of population decline.
The city was the 24th most populous place in the United States as of 2010.
According to data from 2010, commuters from the suburbs increase the District's daytime population to over one million people.
If the District were a state it would rank 49th in population, ahead of Vermont and Wyoming.
The Washington Metropolitan Area, which includes the District and surrounding suburbs, is the sixth-largest metropolitan area in the United States with an estimated 6 million residents in 2014.
When the Washington area is included with Baltimore and its suburbs, the Baltimore–Washington Metropolitan Area had a population exceeding 9.5 million residents in 2014, the fourth-largest combined statistical area in the country.
According to 2015 Census Bureau data, the population of Washington, D.C. was 48.3% Black or African American, 44.1% White (36.1% non-Hispanic White), 4.2% Asian, 0.6% American Indian or Alaska Native, and 0.2% Native Hawaiian or Other Pacific Islander.
Individuals from two or more races made up 2.7% of the population.
Hispanics of any race made up 10.6% of the District's population.
Washington has had a significant African American population since the city's foundation.
African American residents composed about 30% of the District's total population between 1800 and 1940.
The black population reached a peak of 70% by 1970, but has since steadily declined due to many African Americans moving to the surrounding suburbs.
Partly as a result of gentrification, there was a 31.4% increase in the non-Hispanic white population and an 11.5% decrease in the black population between 2000 and 2010.
About 17% of D.C. residents were age 18 or younger in 2010; lower than the U.S. average of 24%.
However, at 34 years old, the District had the lowest median age compared to the 50 states.
As of 2010, there were an estimated 81,734 immigrants living in Washington, D.C. Major sources of immigration include El Salvador, Vietnam, and Ethiopia, with a concentration of Salvadorans in the Mount Pleasant neighborhood.
Researchers found that there were 4,822 same-sex couples in the District of Columbia in 2010; about 2% of total households.
Legislation authorizing same-sex marriage passed in 2009 and the District began issuing marriage licenses to same-sex couples in March 2010.
A 2007 report found that about one-third of District residents were functionally illiterate, compared to a national rate of about one in five.
This is attributed in part to immigrants who are not proficient in English.
As of 2011, 85% of D.C. residents age 5 and older spoke English at home as a primary language.
Half of residents had at least a four-year college degree in 2006.
D.C. residents had a personal income per capita of $55,755; higher than any of the 50 states.
However, 19% of residents were below the poverty level in 2005, higher than any state except Mississippi.
Of the District's population, 17% is Baptist, 13% is Catholic, 6% is Evangelical Protestant, 4% is Methodist, 3% is Episcopalian/Anglican, 3% is Jewish, 2% is Eastern Orthodox, 1% is Pentecostal, 1% is Buddhist, 1% is Adventist, 1% is Lutheran, 1% is Muslim, 1% is Presbyterian, 1% is Mormon, and 1% is Hindu.
Over 90% of D.C. residents have health insurance coverage, the second-highest rate in the nation.
This is due in part to city programs that help provide insurance to low-income individuals who do not qualify for other types of coverage.
A 2009 report found that at least 3% of District residents have HIV or AIDS, which the Centers for Disease Control and Prevention (CDC) characterizes as a "generalized and severe" epidemic.
Crime
Crime in Washington, D.C., is concentrated in areas associated with poverty, drug abuse, and gangs.
A 2010 study found that 5% of city blocks accounted for over one-quarter of the District's total crime.
The more affluent neighborhoods of Northwest Washington are typically safe, but reports of violent crime increase in poorer neighborhoods generally concentrated in the eastern portion of the city.
Approximately 60,000 residents are ex-convicts.
Washington was often described as the "murder capital" of the United States during the early 1990s.
The number of murders peaked in 1991 at 479, but the level of violence then began to decline significantly.
By 2012, Washington's annual murder count had dropped to 88, the lowest total since 1961.
The murder rate has since risen from that historic low, though it remains close to half the rate of the early 2000s.
In 2016, the District's Metropolitan Police Department tallied 135 homicides, a 53% increase from 2012 but a 17% decrease from 2015.
Many neighborhoods such as Columbia Heights and Logan Circle are becoming safer and vibrant.
However, incidents of robberies and thefts have remained higher in these areas because of increased nightlife activity and greater numbers of affluent residents.
Even still, citywide reports of both property and violent crimes have declined by nearly half since their most recent highs in the mid-1990s.
On June 26, 2008, the Supreme Court of the United States held in District of Columbia v. Heller that the city's 1976 handgun ban violated the Second Amendment right to gun ownership.
However, the ruling does not prohibit all forms of gun control; laws requiring firearm registration remain in place, as does the city's assault weapon ban.
In addition to the District's own Metropolitan Police Department, many federal law enforcement agencies have jurisdiction in the city as well; most visibly the U.S. Park Police, founded in 1791.
Washington has a growing, diversified economy with an increasing percentage of professional and business service jobs.
The gross state product of the District in 2010 was $103.3 billion, which would rank it No.
34 compared to the 50 states.
The gross product of the Washington Metropolitan Area was $425 billion in 2010, making it the fourth-largest metropolitan economy in the United States.
As of June 2011, the Washington Metropolitan Area had an unemployment rate of 6.2%; the second-lowest rate among the 49 largest metro areas in the nation.
The District of Columbia itself had an unemployment rate of 9.8% during the same time period.
In 2012, the federal government accounted for about 29% of the jobs in Washington, D.C.
This is thought to immunize Washington to national economic downturns because the federal government continues operations even during recessions.
Many organizations such as law firms, independent contractors (both defense and civilian), non-profit organizations, lobbying firms, trade unions, industry trade groups, and professional associations have their headquarters in or near D.C. to be close to the federal government.
Tourism is Washington's second largest industry.
Approximately 18.9 million visitors contributed an estimated $4.8 billion to the local economy in 2012.
The District also hosts nearly 200 foreign embassies and international organizations such as the World Bank, the International Monetary Fund (IMF), the Organization of American States, the Inter-American Development Bank, and the Pan American Health Organization.
In 2008, the foreign diplomatic corps in Washington employed about 10,000 people and contributed an estimated $400 million annually to the local economy.
The District has growing industries not directly related to government, especially in the areas of education, finance, public policy, and scientific research.
Georgetown University, George Washington University, Washington Hospital Center, Children's National Medical Center and Howard University are the top five non-government-related employers in the city as of 2009.
According to statistics compiled in 2011, four of the largest 500 companies in the country were headquartered in the District.
Historic sites and museums
The National Mall is a large, open park in downtown Washington between the Lincoln Memorial and the United States Capitol.
Given its prominence, the mall is often the location of political protests, concerts, festivals, and presidential inaugurations.
The Washington Monument and the Jefferson Pier are near the center of the mall, south of the White House.
Also on the mall are the National World War II Memorial at the east end of the Lincoln Memorial Reflecting Pool, the Korean War Veterans Memorial, and the Vietnam Veterans Memorial.
Directly south of the mall, the Tidal Basin features rows of Japanese cherry blossom trees that originated as gifts from the nation of Japan.
The Franklin Delano Roosevelt Memorial, George Mason Memorial, Jefferson Memorial, Martin Luther King Jr. Memorial, and the District of Columbia War Memorial are around the Tidal Basin.
The National Archives houses thousands of documents important to American history including the Declaration of Independence, the United States Constitution, and the Bill of Rights.
Located in three buildings on Capitol Hill, the Library of Congress is the largest library complex in the world with a collection of over 147 million books, manuscripts, and other materials.
The United States Supreme Court Building was completed in 1935; before then, the court held sessions in the Old Senate Chamber of the Capitol.
The Smithsonian Institution is an educational foundation chartered by Congress in 1846 that maintains most of the nation's official museums and galleries in Washington, D.C.
The U.S. government partially funds the Smithsonian and its collections open to the public free of charge.
The Smithsonian's locations had a combined total of 30 million visits in 2013.
The most visited museum is the National Museum of Natural History on the National Mall.
Other Smithsonian Institution museums and galleries on the mall are: the National Air and Space Museum; the National Museum of African Art; the National Museum of American History; the National Museum of the American Indian; the Sackler and Freer galleries, which both focus on Asian art and culture; the Hirshhorn Museum and Sculpture Garden; the Arts and Industries Building; the S. Dillon Ripley Center; and the Smithsonian Institution Building (also known as "The Castle"), which serves as the institution's headquarters.
The Smithsonian American Art Museum and the National Portrait Gallery are housed in the Old Patent Office Building, near Washington's Chinatown.
The Renwick Gallery is officially part of the Smithsonian American Art Museum but is in a separate building near the White House.
Other Smithsonian museums and galleries include: the Anacostia Community Museum in Southeast Washington; the National Postal Museum near Union Station; and the National Zoo in Woodley Park.
The National Gallery of Art is on the National Mall near the Capitol and features works of American and European art.
The gallery and its collections are owned by the U.S. government but are not a part of the Smithsonian Institution.
The National Building Museum, which occupies the former Pension Building near Judiciary Square, was chartered by Congress and hosts exhibits on architecture, urban planning, and design.
There are many private art museums in the District of Columbia, which house major collections and exhibits open to the public such as the National Museum of Women in the Arts; the Corcoran Gallery of Art, the largest private museum in Washington; and The Phillips Collection in Dupont Circle, the first museum of modern art in the United States.
Other private museums in Washington include the Newseum, the O Street Museum Foundation, the International Spy Museum, the National Geographic Society Museum, and the Marian Koshland Science Museum.
The United States Holocaust Memorial Museum near the National Mall maintains exhibits, documentation, and artifacts related to the Holocaust.
Arts
Washington, D.C., is a national center for the arts.
The John F. Kennedy Center for the Performing Arts is home to the National Symphony Orchestra, the Washington National Opera, and the Washington Ballet.
The Kennedy Center Honors are awarded each year to those in the performing arts who have contributed greatly to the cultural life of the United States.
The historic Ford's Theatre, site of the assassination of President Abraham Lincoln, continues to operate as a functioning performance space as well as museum.
The Marine Barracks near Capitol Hill houses the United States Marine Band; founded in 1798, it is the country's oldest professional musical organization.
American march composer and Washington-native John Philip Sousa led the Marine Band from 1880 until 1892.
Founded in 1925, the United States Navy Band has its headquarters at the Washington Navy Yard and performs at official events and public concerts around the city.
Washington has a strong local theater tradition.
Founded in 1950, Arena Stage achieved national attention and spurred growth in the city's independent theater movement that now includes organizations such as the Shakespeare Theatre Company, Woolly Mammoth Theatre Company, and the Studio Theatre.
Arena Stage opened its newly renovated home in the city's emerging Southwest waterfront area in 2010.
The GALA Hispanic Theatre, now housed in the historic Tivoli Theatre in Columbia Heights, was founded in 1976 and is a National Center for the Latino Performing Arts.
The U Street Corridor in Northwest D.C., known as "Washington's Black Broadway", is home to institutions like the Howard Theatre, Bohemian Caverns, and the Lincoln Theatre, which hosted music legends such as Washington-native Duke Ellington, John Coltrane, and Miles Davis.
Washington has its own native music genre called go-go; a post-funk, percussion-driven flavor of rhythm and blues that was popularized in the late 1970s by D.C. band leader Chuck Brown.
The District is an important center for indie culture and music in the United States.
The label Dischord Records, formed by Ian MacKaye, was one of the most crucial independent labels in the genesis of 1980s punk and eventually indie rock in the 1990s.
Modern alternative and indie music venues like The Black Cat and the 9:30 Club bring popular acts to the U Street area.
Sports
Washington is one of 12 cities in the United States with teams from all four major professional men's sports and is home to one major professional women's team.
The Washington Wizards (National Basketball Association), the Washington Capitals (National Hockey League), and the Washington Mystics (Women's National Basketball Association), play at the Verizon Center in Chinatown.
Nationals Park, which opened in Southeast D.C. in 2008, is home to the Washington Nationals (Major League Baseball).
D.C. United (Major League Soccer) plays at RFK Stadium.
The Washington Redskins (National Football League) play at nearby FedExField in Landover, Maryland.
Current D.C. teams have won a combined ten professional league championships: the Washington Redskins have won five; D.C. United has won four; and the Washington Wizards (then the Washington Bullets) have won a single championship.
Other professional and semi-professional teams in Washington include: the Washington Kastles (World TeamTennis); the Washington D.C. Slayers (USA Rugby League); the Baltimore Washington Eagles (U.S. Australian Football League); the D.C. Divas (Independent Women's Football League); and the Potomac Athletic Club RFC (Rugby Super League).
The William H.G.
FitzGerald Tennis Center in Rock Creek Park hosts the Citi Open.
Washington is also home to two major annual marathon races: the Marine Corps Marathon, which is held every autumn, and the Rock 'n' Roll USA Marathon held in the spring.
The Marine Corps Marathon began in 1976 and is sometimes called "The People's Marathon" because it is the largest marathon that does not offer prize money to participants.
The District's four NCAA Division I teams, American Eagles, George Washington Colonials, Georgetown Hoyas and Howard Bison and Lady Bison, have a broad following.
The Georgetown Hoyas men's basketball team is the most notable and also plays at the Verizon Center.
From 2008 to 2012, the District hosted an annual college football bowl game at RFK Stadium, called the Military Bowl.
The D.C. area is home to one regional sports television network, Comcast SportsNet (CSN), based in Bethesda, Maryland.
Washington, D.C. is a prominent center for national and international media.
The Washington Post, founded in 1877, is the oldest and most-read local daily newspaper in Washington.
It is probably most notable for its coverage of national and international politics and for exposing the Watergate scandal.
"The Post", as it is popularly called, had the sixth-highest readership of all news dailies in the country in 2011.
The Washington Post Company also publishes a daily free commuter newspaper called the Express, which summarizes events, sports and entertainment, as well as the Spanish-language paper El Tiempo Latino.
Another popular local daily is The Washington Times, the city's second general interest broadsheet and also an influential paper in political circles.
The alternative weekly Washington City Paper also have substantial readership in the Washington area.
Some community and specialty papers focus on neighborhood and cultural issues, including the weekly Washington Blade and Metro Weekly, which focus on LGBT issues; the Washington Informer and The Washington Afro American, which highlight topics of interest to the black community; and neighborhood newspapers published by The Current Newspapers.
Congressional Quarterly, The Hill, Politico and Roll Call newspapers focus exclusively on issues related to Congress and the federal government.
Other publications based in Washington include the National Geographic magazine and political publications such as The Washington Examiner, The New Republic and Washington Monthly.
The Washington Metropolitan Area is the ninth-largest television media market in the nation, with two million homes, approximately 2% of the country's population.
Several media companies and cable television channels have their headquarters in the area, including C-SPAN; Black Entertainment Television (BET); Radio One; the National Geographic Channel; Smithsonian Networks; National Public Radio (NPR); Travel Channel (in Chevy Chase, Maryland); Discovery Communications (in Silver Spring, Maryland); and the Public Broadcasting Service (PBS) (in Arlington, Virginia).
The headquarters of Voice of America, the U.S. government's international news service, is near the Capitol in Southwest Washington.
Politics
Article One, Section Eight of the United States Constitution grants the United States Congress "exclusive jurisdiction" over the city.
The District did not have an elected local government until the passage of the 1973 Home Rule Act.
The Act devolved certain Congressional powers to an elected mayor, currently Muriel Bowser, and the thirteen-member Council of the District of Columbia.
However, Congress retains the right to review and overturn laws created by the council and intervene in local affairs.
Each of the city's eight wards elects a single member of the council and residents elect four at-large members to represent the District as a whole.
The council chair is also elected at-large.
There are 37 Advisory Neighborhood Commissions (ANCs) elected by small neighborhood districts.
ANCs can issue recommendations on all issues that affect residents; government agencies take their advice under careful consideration.
The Attorney General of the District of Columbia, currently Karl Racine, is elected to a four-year term.
Washington, D.C., observes all federal holidays and also celebrates Emancipation Day on April 16, which commemorates the end of slavery in the District.
The flag of Washington, D.C., was adopted in 1938 and is a variation on George Washington's family coat of arms.
Budgetary issues
The mayor and council set local taxes and a budget, which must be approved by Congress.
The Government Accountability Office and other analysts have estimated that the city's high percentage of tax-exempt property and the Congressional prohibition of commuter taxes create a structural deficit in the District's local budget of anywhere between $470 million and over $1 billion per year.
Congress typically provides additional grants for federal programs such as Medicaid and the operation of the local justice system; however, analysts claim that the payments do not fully resolve the imbalance.
The city's local government, particularly during the mayoralty of Marion Barry, was criticized for mismanagement and waste.
During his administration in 1989, The Washington Monthly magazine claimed that the District had "the worst city government in America."
In 1995, at the start of Barry's fourth term, Congress created the District of Columbia Financial Control Board to oversee all municipal spending.
Mayor Anthony Williams won election in 1998 and oversaw a period of urban renewal and budget surpluses.
The District regained control over its finances in 2001 and the oversight board's operations were suspended.
Voting rights debate
The District is not a state and therefore has no voting representation in the Congress.
D.C. residents elect a non-voting delegate to the House of Representatives, currently Eleanor Holmes Norton (D-D.C. At-Large), who may sit on committees, participate in debate, and introduce legislation, but cannot vote on the House floor.
The District has no official representation in the United States Senate.
Neither chamber seats the District's elected "shadow" representative or senators.
Unlike residents of U.S. territories such as Puerto Rico or Guam, which also have non-voting delegates, D.C. residents are subject to all federal taxes.
In the financial year 2012, D.C. residents and businesses paid $20.7 billion in federal taxes; more than the taxes collected from 19 states and the highest federal taxes per capita.
A 2005 poll found that 78% of Americans did not know that residents of the District of Columbia have less representation in Congress than residents of the 50 states.
Efforts to raise awareness about the issue have included campaigns by grassroots organizations and featuring the city's unofficial motto, "Taxation Without Representation", on D.C. vehicle license plates.
There is evidence of nationwide approval for D.C. voting rights; various polls indicate that 61 to 82% of Americans believe that D.C. should have voting representation in Congress.
Despite public support, attempts to grant the District voting representation, including the D.C. statehood movement and the proposed District of Columbia Voting Rights Amendment, have been unsuccessful.
Opponents of D.C. voting rights propose that the Founding Fathers never intended for District residents to have a vote in Congress since the Constitution makes clear that representation must come from the states.
Those opposed to making D.C. a state claim that such a move would destroy the notion of a separate national capital and that statehood would unfairly grant Senate representation to a single city.
Sister cities
Washington, D.C., has fourteen official sister city agreements.
Listed in the order each agreement was first established, they are: Bangkok, Thailand (1962, renewed 2002); Dakar, Senegal (1980, renewed 2006); Beijing, China (1984, renewed 2004); Brussels, Belgium (1985, renewed 2002); Athens, Greece (2000); Paris, France (2000 as a friendship and cooperation agreement, renewed 2005); Pretoria, South Africa (2002, renewed 2008); Seoul, South Korea (2006); Accra, Ghana (2006); Sunderland, United Kingdom (2006); Rome, Italy (2011); Ankara, Turkey (2011); Brasília, Brazil (2013); and Addis Ababa, Ethiopia (2013).
Each of the listed cities is a national capital except for Sunderland, which includes the town of Washington, the ancestral home of George Washington's family.
Paris and Rome are each formally recognized as a "partner city" due to their special one sister city policy.
District of Columbia Public Schools (DCPS) operates the city's 123 public schools.
The number of students in DCPS steadily decreased for 39 years until 2009.
In the 2010–11 school year, 46,191 students were enrolled in the public school system.
DCPS has one of the highest-cost yet lowest-performing school systems in the country, both in terms of infrastructure and student achievement.
Mayor Adrian Fenty's administration made sweeping changes to the system by closing schools, replacing teachers, firing principals, and using private education firms to aid curriculum development.
The District of Columbia Public Charter School Board monitors the 52 public charter schools in the city.
Due to the perceived problems with the traditional public school system, enrollment in public charter schools has steadily increased.
As of fall 2010, D.C. charter schools had a total enrollment of about 32,000, a 9% increase from the prior year.
The District is also home to 92 private schools, which enrolled approximately 18,000 students in 2008.
The District of Columbia Public Library operates 25 neighborhood locations including the landmark Martin Luther King Jr. Memorial Library.
Private universities include American University (AU), the Catholic University of America (CUA), Gallaudet University, George Washington University (GW), Georgetown University (GU), Howard University, and the Johns Hopkins University School of Advanced International Studies (SAIS).
The Corcoran College of Art and Design provides specialized arts instruction and other higher-education institutions offer continuing, distance and adult education.
The University of the District of Columbia (UDC) is a public university providing undergraduate and graduate education.
D.C. residents may also be eligible for a grant of up to $10,000 per year to offset the cost of tuition at any public university in the country.
The District is known for its medical research institutions such as Washington Hospital Center and the Children's National Medical Center, as well as the National Institutes of Health in Bethesda, Maryland.
In addition, the city is home to three medical schools and associated teaching hospitals at George Washington, Georgetown, and Howard universities.
Transportation
There are 1,500 miles (2,400 km) of streets, parkways, and avenues in the District.
Due to the freeway revolts of the 1960s, much of the proposed interstate highway system through the middle of Washington was never built.
Interstate 95 (I-95), the nation's major east coast highway, therefore bends around the District to form the eastern portion of the Capital Beltway.
A portion of the proposed highway funding was directed to the region's public transportation infrastructure instead.
The interstate highways that continue into Washington, including I-66 and I-395, both terminate shortly after entering the city.
The Washington Metropolitan Area Transit Authority (WMATA) operates the Washington Metro, the city's rapid transit system, as well as Metrobus.
Both systems serve the District and its suburbs.
Metro opened on March 27, 1976 and, as of July 2014, consists of 91 stations and 117 miles (188 km) of track.
With an average of about one million trips each weekday, Metro is the second-busiest rapid transit system in the country.
Metrobus serves over 400,000 riders each weekday and is the nation's fifth-largest bus system.
The city also operates its own DC Circulator bus system, which connects commercial areas within central Washington.
Union Station is the city's main train station and services approximately 70,000 people each day.
It is Amtrak's second-busiest station with 4.6 million passengers annually and is the southern terminus for the Northeast Corridor and Acela Express routes.
Maryland's MARC and Virginia's VRE commuter trains and the Metrorail Red Line also provide service into Union Station.
Following renovations in 2011, Union Station became Washington's primary intercity bus transit center.
Three major airports serve the District.
Ronald Reagan Washington National Airport is across the Potomac River from downtown Washington in Arlington, Virginia and primarily handles domestic flights.
Major international flights arrive and depart from Washington Dulles International Airport, 26.3 miles (42.3 km) west of the District in Fairfax and Loudoun counties in Virginia.
Baltimore-Washington International Thurgood Marshall Airport is 31.7 miles (51.0 km) northeast of the District in Anne Arundel County, Maryland.
According to a 2010 study, Washington-area commuters spent 70 hours a year in traffic delays, which tied with Chicago for having the nation's worst road congestion.
However, 37% of Washington-area commuters take public transportation to work, the second-highest rate in the country.
An additional 12% of D.C. commuters walked to work, 6% carpooled, and 3% traveled by bicycle in 2010.
A 2011 study by Walk Score found that Washington was the seventh-most walkable city in the country with 80% of residents living in neighborhoods that are not car dependent.
An expected 32% increase in transit usage within the District by 2030 has spurred construction of a new DC Streetcar system to interconnect the city's neighborhoods.
Construction has also started on an additional Metro line that will connect Washington to Dulles airport.
The District is part of the regional Capital Bikeshare program.
Started in 2010, it is currently one of the largest bicycle sharing systems in the country with over 4,351 bicycles and more than 395 stations all provided by PBSC Urban Solutions.
The city is expanding a network of marked bicycle lanes which currently exist on 56 miles (90 km) of streets.
Utilities
The District of Columbia Water and Sewer Authority (i.e.
WASA or D.C. Water) is an independent authority of the D.C. government that provides drinking water and wastewater collection in Washington.
WASA purchases water from the historic Washington Aqueduct, which is operated by the Army Corps of Engineers.
The water, sourced from the Potomac River, is treated and stored in the city's Dalecarlia, Georgetown, and McMillan reservoirs.
The aqueduct provides drinking water for a total of 1.1 million people in the District and Virginia, including Arlington, Falls Church, and a portion of Fairfax County.
The authority also provides sewage treatment services for an additional 1.6 million people in four surrounding Maryland and Virginia counties.
Pepco is the city's electric utility and services 793,000 customers in the District and suburban Maryland.
An 1889 law prohibits overhead wires within much of the historic City of Washington.
As a result, all power lines and telecommunication cables are located underground in downtown Washington, and traffic signals are placed at the edge of the street.
A plan announced in 2013 would bury an additional 60 miles (97 km) of primary power lines throughout the District.
Washington Gas is the city's natural gas utility and serves over one million customers in the District and its suburbs.
Incorporated by Congress in 1848, the company installed the city's first gas lights in the Capitol,the White House, and along Pennsylvania Avenue.
Arts and culture of Washington, D.C.
Category:People from Washington, D.C.
Index of Washington, D.C.-related articles
Outline of Washington, D.C.
Notes
References
External links
Official website
Guide to Washington, D.C., materials from the Library of Congress
Geographic data related to Washington, D.C. at OpenStreetMap
U.S. Geological Survey Geographic Names Information System: District of Columbia (civil)
Washington, D.C. at the Wayback Machine (archived March 31, 2001)
	"""


	# for sent in tokenize_sent(sent1):
	# 	print sent
	# for word in tokenize_sent_to_words(sent1):
	# 	print word
	# for word in tokenized_to_words(sent3):
	# 	print word


	print read_from_txt("/home/yiting/Dropbox/ThingsStrings/Things_and_Strings/training_data/wikipedia/Washington/Washington,_District_of_Columbia.txt")