import json
import time
import os
from sklearn import metrics
#import datetime
import sklearn
from sklearn.model_selection import train_test_split, permutation_test_score
from sklearn.tree import DecisionTreeRegressor
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import requests
from datetime import datetime , timedelta
import pandas as pd
import sklearn as sc
import numpy as np
import matplotlib as mat
from matplotlib import pyplot as plt
import seaborn as sb

from .models import User, Queries
airlinecodes = {'WN':'19393.0',
 'YV':'20378.0',
 'YX':'20452.0',
 '9E':'20363.0',
 'AA':'19805.0',
 'OO':'20304.0',
 'QX':'19687.0',
 'UA':'19977.0',
 'C5':'20445.0',
 'G7':'20500.0',
 'ZW':'20046.0',
 'DL':'19790.0',
 'F9':'20436.0',
 'G4':'20368.0',
 'HA':'19690.0',
 'EM':'20263.0',
 'MQ':'20398.0',
 'NK':'20416.0',
 'OH':'20397.0',
 'PT':'20427.0',
 'AS':'19930.0',
 'B6':'20409.0',
 'EV':'20366.0'}
 
airportcodes = {'DAL':'11259',
 'DCA':'11278',
 'DEN':'11292',
 'DSM':'11423',
 'DTW':'11433',
 'ECP':'11481',
 'ELP':'11540',
 'FLL':'11697',
 'GEG':'11884',
 'GRR':'11986',
 'GSP':'11996',
 'HDN':'12094',
 'HNL':'12173',
 'HOU':'12191',
 'HRL':'12206',
 'IAD':'12264',
 'ICT':'12278',
 'IND':'12339',
 'ISP':'12391',
 'ITO':'12402',
 'JAX':'12451',
 'KOA':'12758',
 'LAS':'12889',
 'LAX':'12892',
 'LBB':'12896',
 'LGA':'12953',
 'LGB':'12954',
 'LIH':'12982',
 'LIT':'12992',
 'MAF':'13158',
 'MCI':'13198',
 'MCO':'13204',
 'MDW':'13232',
 'MEM':'13244',
 'MHT':'13296',
 'MIA':'13303',
 'MKE':'13342',
 'MSP':'13487',
 'MSY':'13495',
 'MTJ':'13502',
 'OAK':'13796',
 'OGG':'13830',
 'OKC':'13851',
 'OMA':'13871',
 'ONT':'13891',
 'ORF':'13931',
 'PBI':'14027',
 'PDX':'14057',
 'PHL':'14100',
 'PHX':'14107',
 'PIT':'14122',
 'PNS':'14193',
 'PSP':'14262',
 'PVD':'14307',
 'PWM':'14321',
 'RDU':'14492',
 'RIC':'14524',
 'RNO':'14570',
 'ROC':'14576',
 'RSW':'14635',
 'SAN':'14679',
 'SAT':'14683',
 'SDF':'14730',
 'SEA':'14747',
 'SFO':'14771',
 'SJC':'14831',
 'SJU':'14843',
 'SLC':'14869',
 'SMF':'14893',
 'SNA':'14908',
 'STL':'15016',
 'TPA':'15304',
 'TUL':'15370',
 'TUS':'15376',
 'ABQ':'10140',
 'ALB':'10257',
 'AMA':'10279',
 'ATL':'10397',
 'AUS':'10423',
 'BDL':'10529',
 'BHM':'10599',
 'BNA':'10693',
 'BOI':'10713',
 'BOS':'10721',
 'BUF':'10792',
 'BUR':'10800',
 'BWI':'10821',
 'CHS':'10994',
 'CLE':'11042',
 'CLT':'11057',
 'CMH':'11066',
 'CRP':'11140',
 'CVG':'11193',
 'SAV':'14685',
 'IAH':'12266',
 'MFE':'13256',
 'DFW':'11298',
 'SRQ':'14986',
 'GUC':'12012',
 'BZN':'10849',
 'XNA':'15919',
 'EYW':'11624',
 'BTV':'10785',
 'BTR':'10781',
 'MOB':'13422',
 'SYR':'15096',
 'VPS':'15624',
 'TYS':'15412',
 'MRY':'13476',
 'STS':'15023',
 'AVL':'10431',
 'MSN':'13485',
 'PIA':'14108',
 'MLI':'13367',
 'FLG':'11695',
 'ILM':'12323',
 'RAP':'14457',
 'SBA':'14689',
 'TLH':'15249',
 'LFT':'12951',
 'BFL':'10561',
 'GSO':'11995',
 'FAT':'11638',
 'YUM':'16218',
 'FSD':'11775',
 'FAR':'11637',
 'DAB':'11252',
 'ORD':'13930',
 'HVN':'12244',
 'BGR':'10581',
 'HHH':'12124',
 'MYR':'13577',
 'EWR':'11618',
 'ATW':'10408',
 'JFK':'12478',
 'LEX':'12945',
 'CAE':'10868',
 'LNK':'13029',
 'CID':'11003',
 'CHA':'10980',
 'GRB':'11977',
 'TVC':'15380',
 'ROA':'14574',
 'DLH':'11337',
 'MDT':'13230',
 'CHO':'10990',
 'TRI':'15323',
 'VLD':'15607',
 'ABE':'10135',
 'JAN':'12448',
 'AZO':'10469',
 'OAJ':'13795',
 'RST':'14633',
 'GPT':'11973',
 'GNV':'11953',
 'DHN':'11308',
 'HSV':'12217',
 'BIS':'10627',
 'MGM':'13277',
 'AGS':'10208',
 'EVV':'11612',
 'SBN':'14696',
 'ABY':'10146',
 'MBS':'13184',
 'MOT':'13433',
 'DAY':'11267',
 'BMI':'10685',
 'SGF':'14783',
 'BQK':'10731',
 'FAY':'11641',
 'CRW':'11146',
 'CSG':'11150',
 'BGM':'10577',
 'GTR':'12007',
 'AEX':'10185',
 'LAN':'12884',
 'MLU':'13377',
 'ELM':'11537',
 'CWA':'11203',
 'GFK':'11898',
 'SHV':'14814',
 'SCE':'14711',
 'ITH':'12397',
 'FWA':'11823',
 'STT':'15024',
 'EGE':'11503',
 'STX':'15027',
 'COS':'11109',
 'EUG':'11603',
 'MFR':'13264',
 'SUN':'15041',
 'GJT':'11921',
 'JAC':'12441',
 'LWS':'13127',
 'INL':'12343',
 'ESC':'11587',
 'GTF':'12003',
 'TWF':'15389',
 'SGU':'14794',
 'EKO':'11525',
 'LSE':'13076',
 'PIH':'14113',
 'BRD':'10739',
 'ABR':'10141',
 'APN':'10333',
 'CIU':'11013',
 'RHI':'14520',
 'IMT':'12335',
 'BTM':'10779',
 'PLN':'14150',
 'BJI':'10631',
 'MQT':'13459',
 'CPR':'11122',
 'RDM':'14489',
 'FCA':'11648',
 'BIL':'10620',
 'MSO':'13486',
 'HLN':'12156',
 'PSC':'14252',
 'IDA':'12280',
 'FAI':'11630',
 'HIB':'12129',
 'CDC':'10918',
 'ASE':'10372',
 'VCT':'15569',
 'CGI':'10967',
 'CMX':'11076',
 'CYS':'11233',
 'SLN':'14877',
 'DVL':'11447',
 'JMS':'12519',
 'PAH':'14006',
 'MKG':'13344',
 'ALS':'10272',
 'LBF':'12899',
 'VEL':'15582',
 'HOB':'12177',
 'SAF':'14674',
 'CKB':'11027',
 'CNY':'11092',
 'JST':'12559',
 'DDC':'11283',
 'SHD':'14802',
 'DIK':'11315',
 'SBP':'14698',
 'PIB':'14109',
 'PIR':'14120',
 'PRC':'14237',
 'RKS':'14543',
 'EAR':'11468',
 'ATY':'10409',
 'OGS':'13832',
 'HYS':'12255',
 'XWA':'16869',
 'DRO':'11413',
 'EAU':'11471',
 'SHR':'14812',
 'PBG':'14025',
 'GCC':'11865',
 'MEI':'13241',
 'LWB':'13121',
 'BFF':'10558',
 'PUB':'14288',
 'DEC':'11288',
 'LAR':'12888',
 'SUX':'15048',
 'FNT':'11721',
 'LBL':'12902',
 'RIW':'14534',
 'ABI':'10136',
 'COD':'11097',
 'PAE':'14004',
 'RDD':'14487',
 'ACV':'10157',
 'OTH':'13964',
 'YKM':'16101',
 'ALW':'10275',
 'PUW':'14303',
 'ANC':'10299',
 'EAT':'11470',
 'BLI':'10666',
 'AKN':'10245',
 'DLG':'11336',
 'GUM':'12016',
 'SPN':'14955',
 'PQI':'14231',
 'LCH':'12915',
 'CLL':'11049',
 'GRK':'11982',
 'CAK':'10874',
 'BRO':'10747',
 'LRD':'13061',
 'SPI':'14952',
 'ERI':'11577',
 'AVP':'10434',
 'COU':'11111',
 'MLB':'13360',
 'TTN':'15356',
 'AZA':'10466',
 'SFB':'14761',
 'LCK':'12917',
 'PGD':'14082',
 'PIE':'14112',
 'STC':'15008',
 'USA':'12544',
 'PVU':'14314',
 'BLV':'10676',
 'IAG':'12265',
 'RFD':'14512',
 'SWF':'15070',
 'SCK':'14716',
 'HGR':'12119',
 'HTS':'12223',
 'OWB':'13983',
 'PSM':'14259',
 'SMX':'14905',
 'OGD':'13829',
 'TOL':'15295',
 'GRI':'11980',
 'MKK':'13347',
 'LNY':'13034',
 'DBQ':'11274',
 'TYR':'15411',
 'ALO':'10268',
 'SJT':'14842',
 'BPT':'10728',
 'MHK':'13290',
 'ACT':'10155',
 'SWO':'15074',
 'GCK':'11867',
 'TXK':'15401',
 'SPS':'14960',
 'GGG':'11905',
 'LAW':'12891',
 'FSM':'11778',
 'CMI':'11067',
 'DRT':'11415',
 'ACY':'10158',
 'LBE':'12898',
 'HPN':'12197',
 'EWN':'11617',
 'PHF':'14098',
 'ROW':'14588',
 'JLN':'12511',
 'SBY':'14704',
 'FLO':'11699',
 'LYH':'13139',
 'PGV':'14092',
 'IPT':'12365',
 'ART':'10361',
 'SCC':'14709',
 'JNU':'12523',
 'YAK':'15991',
 'OME':'13873',
 'BRW':'10754',
 'ADQ':'10170',
 'CDB':'10917',
 'OTZ':'13970',
 'KTN':'12819',
 'WRG':'15841',
 'PSG':'14256',
 'BET':'10551',
 'CDV':'10926',
 'SIT':'14828',
 'ADK':'10165',
 'ACK':'10154',
 'ILG':'12320',
 'FOD':'11725',
 'MCW':'13211',
 'BQN':'10732',
 'PSE':'14254',
 'BKG':'10643',
 'MVY':'13541',
 'GST':'11997',
 'WYS':'15897',
 'HYA':'12250',
 'ORH':'13933'}

hours = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

useful_cols_arrival = ['YEAR', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'OP_CARRIER_AIRLINE_ID', 'ORIGIN_AIRPORT_SEQ_ID', 'DEST_AIRPORT_SEQ_ID', 'Departure_Hour', 'Real_Departure_Hour','TAXI_OUT', 'WHEELS_OFF_MINS', 'AIR_TIME','DISTANCE','HourlyWindSpeed',  'HourlyVisibility','HourlyStationPressure', 'HourlyRelativeHumidity','HourlyPrecipitation', 'HourlyDryBulbTemperature']

useful_cols_departure = ['YEAR', 'MONTH', 'DAY_OF_MONTH', 'DAY_OF_WEEK', 'OP_CARRIER_AIRLINE_ID', 'ORIGIN_AIRPORT_SEQ_ID', 'CRS_DEP_TIME', 'FLIGHTS','DISTANCE','HourlyWindSpeed', 'HourlyVisibility','HourlyStationPressure', 'HourlyRelativeHumidity','HourlyPrecipitation', 'HourlyDryBulbTemperature']


airports = ['Dallas-DAL',
 'Washington-DCA',
 'Denver-DEN',
 'Des Moines-DSM',
 'Detroit-DTW',
 'Panama City-ECP',
 'El Paso-ELP',
 'Fort Lauderdale-FLL',
 'Spokane-GEG',
 'Grand Rapids-GRR',
 'Greer-GSP',
 'Hayden-HDN',
 'Honolulu-HNL',
 'Houston-HOU',
 'Harlingen/San Benito-HRL',
 'Washington-IAD',
 'Wichita-ICT',
 'Indianapolis-IND',
 'Islip-ISP',
 'Hilo-ITO',
 'Jacksonville-JAX',
 'Kona-KOA',
 'Las Vegas-LAS',
 'Los Angeles-LAX',
 'Lubbock-LBB',
 'New York-LGA',
 'Long Beach-LGB',
 'Lihue-LIH',
 'Little Rock-LIT',
 'Midland/Odessa-MAF',
 'Kansas City-MCI',
 'Orlando-MCO',
 'Chicago-MDW',
 'Memphis-MEM',
 'Manchester-MHT',
 'Miami-MIA',
 'Milwaukee-MKE',
 'Minneapolis-MSP',
 'New Orleans-MSY',
 'Montrose/Delta-MTJ',
 'Oakland-OAK',
 'Kahului-OGG',
 'Oklahoma City-OKC',
 'Omaha-OMA',
 'Ontario-ONT',
 'Norfolk-ORF',
 'West Palm Beach/Palm Beach-PBI',
 'Portland-PDX',
 'Philadelphia-PHL',
 'Phoenix-PHX',
 'Pittsburgh-PIT',
 'Pensacola-PNS',
 'Palm Springs-PSP',
 'Providence-PVD',
 'Portland-PWM',
 'Raleigh/Durham-RDU',
 'Richmond-RIC',
 'Reno-RNO',
 'Rochester-ROC',
 'Fort Myers-RSW',
 'San Diego-SAN',
 'San Antonio-SAT',
 'Louisville-SDF',
 'Seattle-SEA',
 'San Francisco-SFO',
 'San Jose-SJC',
 'San Juan-SJU',
 'Salt Lake City-SLC',
 'Sacramento-SMF',
 'Santa Ana-SNA',
 'St. Louis-STL',
 'Tampa-TPA',
 'Tulsa-TUL',
 'Tucson-TUS',
 'Albuquerque-ABQ',
 'Albany-ALB',
 'Amarillo-AMA',
 'Atlanta-ATL',
 'Austin-AUS',
 'Hartford-BDL',
 'Birmingham-BHM',
 'Nashville-BNA',
 'Boise-BOI',
 'Boston-BOS',
 'Buffalo-BUF',
 'Burbank-BUR',
 'Baltimore-BWI',
 'Charleston-CHS',
 'Cleveland-CLE',
 'Charlotte-CLT',
 'Columbus-CMH',
 'Corpus Christi-CRP',
 'Cincinnati-CVG',
 'Savannah-SAV',
 'Houston-IAH',
 'Mission/McAllen/Edinburg-MFE',
 'Dallas/Fort Worth-DFW',
 'Sarasota/Bradenton-SRQ',
 'Gunnison-GUC',
 'Bozeman-BZN',
 'Fayetteville-XNA',
 'Key West-EYW',
 'Burlington-BTV',
 'Baton Rouge-BTR',
 'Mobile-MOB',
 'Syracuse-SYR',
 'Valparaiso-VPS',
 'Knoxville-TYS',
 'Monterey-MRY',
 'Santa Rosa-STS',
 'Asheville-AVL',
 'Madison-MSN',
 'Peoria-PIA',
 'Moline-MLI',
 'Flagstaff-FLG',
 'Wilmington-ILM',
 'Rapid City-RAP',
 'Santa Barbara-SBA',
 'Tallahassee-TLH',
 'Lafayette-LFT',
 'Bakersfield-BFL',
 'Greensboro/High Point-GSO',
 'Fresno-FAT',
 'Yuma-YUM',
 'Sioux Falls-FSD',
 'Fargo-FAR',
 'Daytona Beach-DAB',
 'Chicago-ORD',
 'New Haven-HVN',
 'Bangor-BGR',
 'Hilton Head-HHH',
 'Myrtle Beach-MYR',
 'Newark-EWR',
 'Appleton-ATW',
 'New York-JFK',
 'Lexington-LEX',
 'Columbia-CAE',
 'Lincoln-LNK',
 'Cedar Rapids/Iowa City-CID',
 'Chattanooga-CHA',
 'Green Bay-GRB',
 'Traverse City-TVC',
 'Roanoke-ROA',
 'Duluth-DLH',
 'Harrisburg-MDT',
 'Charlottesville-CHO',
 'Bristol/Johnson City/Kingsport-TRI',
 'Valdosta-VLD',
 'Allentown/Bethlehem/Easton-ABE',
 'Jackson/Vicksburg-JAN',
 'Kalamazoo-AZO',
 'Jacksonville/Camp Lejeune-OAJ',
 'Rochester-RST',
 'Gulfport/Biloxi-GPT',
 'Gainesville-GNV',
 'Dothan-DHN',
 'Huntsville-HSV',
 'Bismarck/Mandan-BIS',
 'Montgomery-MGM',
 'Augusta-AGS',
 'Evansville-EVV',
 'South Bend-SBN',
 'Albany-ABY',
 'Saginaw/Bay City/Midland-MBS',
 'Minot-MOT',
 'Dayton-DAY',
 'Bloomington/Normal-BMI',
 'Springfield-SGF',
 'Brunswick-BQK',
 'Fayetteville-FAY',
 'Charleston/Dunbar-CRW',
 'Columbus-CSG',
 'Binghamton-BGM',
 'Columbus-GTR',
 'Alexandria-AEX',
 'Lansing-LAN',
 'Monroe-MLU',
 'Elmira/Corning-ELM',
 'Mosinee-CWA',
 'Grand Forks-GFK',
 'Shreveport-SHV',
 'State College-SCE',
 'Ithaca/Cortland-ITH',
 'Fort Wayne-FWA',
 'Charlotte Amalie-STT',
 'Eagle-EGE',
 'Christiansted-STX',
 'Colorado Springs-COS',
 'Eugene-EUG',
 'Medford-MFR',
 'Sun Valley/Hailey/Ketchum-SUN',
 'Grand Junction-GJT',
 'Jackson-JAC',
 'Lewiston-LWS',
 'International Falls-INL',
 'Escanaba-ESC',
 'Great Falls-GTF',
 'Twin Falls-TWF',
 'St. George-SGU',
 'Elko-EKO',
 'La Crosse-LSE',
 'Pocatello-PIH',
 'Brainerd-BRD',
 'Aberdeen-ABR',
 'Alpena-APN',
 'Sault Ste. Marie-CIU',
 'Rhinelander-RHI',
 'Iron Mountain/Kingsfd-IMT',
 'Butte-BTM',
 'Pellston-PLN',
 'Bemidji-BJI',
 'Marquette-MQT',
 'Casper-CPR',
 'Bend/Redmond-RDM',
 'Kalispell-FCA',
 'Billings-BIL',
 'Missoula-MSO',
 'Helena-HLN',
 'Pasco/Kennewick/Richland-PSC',
 'Idaho Falls-IDA',
 'Fairbanks-FAI',
 'Hibbing-HIB',
 'Cedar City-CDC',
 'Aspen-ASE',
 'Victoria-VCT',
 'Cape Girardeau-CGI',
 'Hancock/Houghton-CMX',
 'Cheyenne-CYS',
 'Salina-SLN',
 'Devils Lake-DVL',
 'Jamestown-JMS',
 'Paducah-PAH',
 'Muskegon-MKG',
 'Alamosa-ALS',
 'North Platte-LBF',
 'Vernal-VEL',
 'Hobbs-HOB',
 'Santa Fe-SAF',
 'Clarksburg/Fairmont-CKB',
 'Moab-CNY',
 'Johnstown-JST',
 'Dodge City-DDC',
 'Staunton-SHD',
 'Dickinson-DIK',
 'San Luis Obispo-SBP',
 'Hattiesburg/Laurel-PIB',
 'Pierre-PIR',
 'Prescott-PRC',
 'Rock Springs-RKS',
 'Kearney-EAR',
 'Watertown-ATY',
 'Ogdensburg-OGS',
 'Hays-HYS',
 'Williston-XWA',
 'Durango-DRO',
 'Eau Claire-EAU',
 'Sheridan-SHR',
 'Plattsburgh-PBG',
 'Gillette-GCC',
 'Meridian-MEI',
 'Lewisburg-LWB',
 'Scottsbluff-BFF',
 'Pueblo-PUB',
 'Decatur-DEC',
 'Laramie-LAR',
 'Sioux City-SUX',
 'Flint-FNT',
 'Liberal-LBL',
 'Riverton/Lander-RIW',
 'Abilene-ABI',
 'Cody-COD',
 'Everett-PAE',
 'Redding-RDD',
 'Arcata/Eureka-ACV',
 'North Bend/Coos Bay-OTH',
 'Yakima-YKM',
 'Walla Walla-ALW',
 'Pullman-PUW',
 'Anchorage-ANC',
 'Wenatchee-EAT',
 'Bellingham-BLI',
 'King Salmon-AKN',
 'Dillingham-DLG',
 'Guam-GUM',
 'Saipan-SPN',
 'Presque Isle/Houlton-PQI',
 'Lake Charles-LCH',
 'College Station/Bryan-CLL',
 'Killeen-GRK',
 'Akron-CAK',
 'Brownsville-BRO',
 'Laredo-LRD',
 'Springfield-SPI',
 'Erie-ERI',
 'Scranton/Wilkes-Barre-AVP',
 'Columbia-COU',
 'Melbourne-MLB',
 'Trenton-TTN',
 'Phoenix-AZA',
 'Sanford-SFB',
 'Columbus-LCK',
 'Punta Gorda-PGD',
 'St. Petersburg-PIE',
 'St. Cloud-STC',
 'Concord-USA',
 'Provo-PVU',
 'Belleville-BLV',
 'Niagara Falls-IAG',
 'Rockford-RFD',
 'Newburgh/Poughkeepsie-SWF',
 'Stockton-SCK',
 'Hagerstown-HGR',
 'Ashland-HTS',
 'Owensboro-OWB',
 'Portsmouth-PSM',
 'Santa Maria-SMX',
 'Ogden-OGD',
 'Toledo-TOL',
 'Grand Island-GRI',
 'Hoolehua-MKK',
 'Lanai-LNY',
 'Dubuque-DBQ',
 'Tyler-TYR',
 'Waterloo-ALO',
 'San Angelo-SJT',
 'Beaumont/Port Arthur-BPT',
 'Manhattan/Ft. Riley-MHK',
 'Waco-ACT',
 'Stillwater-SWO',
 'Garden City-GCK',
 'Texarkana-TXK',
 'Wichita Falls-SPS',
 'Longview-GGG',
 'Lawton/Fort Sill-LAW',
 'Fort Smith-FSM',
 'Champaign/Urbana-CMI',
 'Del Rio-DRT',
 'Atlantic City-ACY',
 'Latrobe-LBE',
 'White Plains-HPN',
 'New Bern/Morehead/Beaufort-EWN',
 'Newport News/Williamsburg-PHF',
 'Roswell-ROW',
 'Joplin-JLN',
 'Salisbury-SBY',
 'Florence-FLO',
 'Lynchburg-LYH',
 'Greenville-PGV',
 'Williamsport-IPT',
 'Watertown-ART',
 'Deadhorse-SCC',
 'Juneau-JNU',
 'Yakutat-YAK',
 'Nome-OME',
 'Barrow-BRW',
 'Kodiak-ADQ',
 'Cold Bay-CDB',
 'Kotzebue-OTZ',
 'Ketchikan-KTN',
 'Wrangell-WRG',
 'Petersburg-PSG',
 'Bethel-BET',
 'Cordova-CDV',
 'Sitka-SIT',
 'Adak Island-ADK',
 'Nantucket-ACK',
 'Wilmington-ILG',
 'Fort Dodge-FOD',
 'Mason City-MCW',
 'Aguadilla-BQN',
 'Ponce-PSE',
 'Branson-BKG',
 "Martha's Vineyard-MVY",
 'Gustavus-GST',
 'West Yellowstone-WYS',
 'Hyannis-HYA',
 'Worcester-ORH']


airlinedict = { 'Southwest Airlines Co.' : 'WN', 'Mesa Airlines Inc.' : 'YV', 'Republic Airways' : 'YX', 'Endeavor Air Inc.' : '9E', 'American Airlines Inc.' : 'AA', 'SkyWest Airlines Inc.' : 'OO', 'Horizon Air' : 'QX', 'United Air Lines Inc.' : 'UA', 'Commutair Aka Champlain Enterprises, Inc.' : 'C5', 'GoJet Airlines LLC d/b/a United Express' : 'G7', 'Air Wisconsin Airlines Corp' : 'ZW', 'Delta Air Lines Inc.' : 'DL', 'Frontier Airlines Inc.' : 'F9', 'Allegiant Air' : 'G4', 'Hawaiian Airlines Inc.' : 'HA', 'Empire Airlines Inc.' : 'EM', 'Envoy Air' : 'MQ', 'Spirit Air Lines' : 'NK', 'PSA Airlines Inc.' : 'OH', 'Piedmont Airlines' : 'PT', 'Alaska Airlines Inc.' : 'AS', 'JetBlue Airways' : 'B6', 'ExpressJet Airlines Inc.' : 'EV'  }

def index(request):
    airlines = list(airlinedict.keys())
    airlines.sort()
    airports.sort()
    return render(request, "network/index.html", {
    "airlines": airlines, "airports": airports, "hours": hours
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
        
@csrf_exempt
@login_required
def query(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    elif request.method=="POST":
        originairport = request.POST["originairport"]
        destinationairport = request.POST["destinationairport"]
        airline = request.POST["airlines"]
        flighttime = int(request.POST["flighttime"])
        date = request.POST["start"]
        airlinecode = airlinedict[airline]
        origincity = originairport.split("-")[0]
        originairport = originairport.split("-")[1]
        destinationcity = destinationairport.split("-")[0]
        destinationairport = destinationairport.split("-")[1]
        weatherdict = GetWeatherData(origincity, date)
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        dayofmonth = int(date.split("-")[2])
        dayofweek = datetime.strptime(date, '%Y-%m-%d').weekday()
        #Read the Airport CSV and Weather CSV.
        weatherdata = pd.read_csv(os.getcwd()+"\\Weather-Final.csv")
        final = pd.read_csv(os.getcwd()+"\\Cities\\"+ originairport + ".csv")
        
        final["WHEELS_OFF_MINS"] = final["WHEELS_OFF"] - final["DEP_TIME"]
        
        final["CRS_DEP_TIME"] =  final.CRS_DEP_TIME.astype(str)
        final["CRS_DEP_TIME"] = final["CRS_DEP_TIME"].apply( lambda t : "0"*(3-len(t))+t if len(t) < 3 else t )
        final["Departure_Hour"] = final["CRS_DEP_TIME"].apply( lambda t : datetime.strptime(t,'%H%M').strftime('%H'))
        final["Departure_Hour"] = final["Departure_Hour"].astype('int')
        
        final["DEP_TIME"] =  final.CRS_DEP_TIME.astype(str)
        final["DEP_TIME"] = final["DEP_TIME"].apply( lambda t : "0"*(3-len(t))+t if len(t) < 3 else t )
        final["Real_Departure_Hour"] = final["DEP_TIME"].apply( lambda t : datetime.strptime(t,'%H%M').strftime('%H'))
        final["Real_Departure_Hour"] = final["Real_Departure_Hour"].astype('int')
        
        
        final["DEP_TIME"] =  final.CRS_DEP_TIME.astype(str)
        final["DEP_TIME"] = final["DEP_TIME"].apply( lambda t : "0"*(3-len(t))+t if len(t) < 3 else t )
        final["Real_Departure_Hour"] = final["DEP_TIME"].apply( lambda t : datetime.strptime(t,'%H%M').strftime('%H'))
        final["Real_Departure_Hour"] = final["Real_Departure_Hour"].astype('int')
        
        airportweather = weatherdata[ ( weatherdata["iata_code"]  == originairport )]
        #jdf = final[ ( final["ORIGIN"]  == "JFK" )]

        res = pd.merge(final, airportweather ,  how='left', left_on=['FL_DATE','ORIGIN' , 'Departure_Hour'], right_on = ['DATE','iata_code' , 'Hour'])
        res.fillna(0, inplace=True)
        
        taxiout = res["TAXI_OUT"].mean()
        wheelsoff = res["WHEELS_OFF_MINS"].mean()
        distance = res["DISTANCE"].mean()
        airtime = res["AIR_TIME"].mean()
        realflighttime = int(flighttime + (taxiout/60) + (wheelsoff/60))
        if weatherdict != "No Weather Data":
            hourlywindspeed = weatherdict["HourlyWindSpeed"]
            hourlyvisibility = weatherdict["HourlyVisibility"]
            hourlystationpressure = weatherdict["HourlyStationPressure"]
            hourlyrelativehumidity = weatherdict["HourlyRelativeHumidity"]
            hourlyprecipitation = weatherdict["HourlyPrecipitation"]
            hourlydrybulbtemp = weatherdict["HourlyDryBulbTemperature"]
        else:
            hourlywindspeed = 0
            hourlyvisibility = 0
            hourlystationpressure = 0
            hourlyrelativehumidity = 0
            hourlyprecipitation = 0
            hourlydrybulbtemp = 0
        opcarrierairlineid = airlinecodes[airlinecode]
        print("All variables accounted for.")
        
        #Here, we train our Linear Regression model on the called feature and calculate the RMSE and P-value.

        X = res[useful_cols_arrival]
        y = res['ARR_DELAY']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)
        dt = DecisionTreeRegressor(random_state = 0).fit(X_train, y_train)
        testPred_rf = dt.predict(X_test)
        print("Model Trained successfully")
        
        # R squared value
        variancescore = metrics.explained_variance_score(y_test, testPred_rf)
        r2_score = metrics.r2_score(y_test, testPred_rf)
        
        mean_absolute_error = metrics.mean_absolute_error(y_test, testPred_rf)
        mean_squared_error = metrics.mean_squared_error(y_test, testPred_rf)
        root_mean_squared_error = np.sqrt(metrics.mean_squared_error(y_test, testPred_rf))
        
        realTestdf = pd.DataFrame(columns = useful_cols_arrival)
        realTestdf = realTestdf.append({'YEAR': year, 'MONTH': month,'DAY_OF_MONTH': dayofmonth,'DAY_OF_WEEK': dayofweek,'OP_CARRIER_AIRLINE_ID': opcarrierairlineid,'ORIGIN_AIRPORT_SEQ_ID': airportcodes[originairport],'DEST_AIRPORT_SEQ_ID': airportcodes[destinationairport],'Departure_Hour': flighttime,'Real_Departure_Hour': realflighttime,'TAXI_OUT': taxiout,'WHEELS_OFF_MINS': wheelsoff, 'AIR_TIME': airtime,'DISTANCE': distance,'HourlyWindSpeed': hourlywindspeed,'HourlyVisibility': hourlyvisibility,'HourlyStationPressure': hourlystationpressure,'HourlyRelativeHumidity': hourlyrelativehumidity,'HourlyPrecipitation': hourlyprecipitation,'HourlyDryBulbTemperature': hourlydrybulbtemp,}, ignore_index=True)
        prediction = dt.predict(realTestdf)
        if prediction[0]<0:
            myflag = -1
            prediction[0] = abs(prediction[0])
        elif prediction[0] == 0:
            myflag = 0
        else:
            myflag = 1
        return render(request, "network/results.html", {
            "originairport": originairport, "destinationairport": destinationairport, "airline": airline, "date": date, "prediction": prediction[0], "variancescore": variancescore, "mean_absolute_error": mean_absolute_error, "mean_squared_error": mean_squared_error, "root_mean_squared_error": root_mean_squared_error, "r2_score": r2_score, "myflag": myflag
        })
        
        
def GetWeatherData(city , Current_date):

    API_KEY = "7a9fa0885b884ad5fc2bb986521a0347"

    URL = "http://api.openweathermap.org/data/2.5/forecast/?q="+city+"&appid="+API_KEY+"&units=Imperial"

    response = requests.get(URL)

    data = response.json()

    if "list" in data:

        opt = {}
        dt = datetime.strptime(Current_date, '%Y-%m-%d') + timedelta(hours=5)
        mn = timedelta(days=6)
        #print(data["city"]["name"])
        for row in data["list"]:
        #print(row["dt"])
    
            ct = datetime.utcfromtimestamp(row["dt"])#.strftime('%Y-%m-%d %H:%M:%S')
   
            diff = ct - dt if ct > dt else dt - ct
            if diff < mn:
                mn = diff
                opt["Date"] = ct.strftime('%Y-%m-%d %H:%M:%S')
                opt["HourlyDryBulbTemperature"] = float(row["main"]["temp"])
                opt["HourlyStationPressure"] = float( ( 3 * row["main"]["pressure"] ) / 100 )
                opt["HourlyRelativeHumidity"] = float( row["main"]["humidity"])
                opt["HourlySkyConditions"] = row["weather"][0]["main"]
                opt["HourlyWindSpeed"] = float( row["wind"]["speed"])
                opt["HourlyVisibility"] = float ( row["visibility"] / 1852 )
                opt["HourlyPrecipitation"] = row["pop"]
                if "snow" in row:
                    opt["snowfall"] = row["snow"]["3h"]
                if "rain" in row:
                    opt["rainfall"] = row["rain"]["3h"]

        return opt

    else:

        return "No Weather Data"