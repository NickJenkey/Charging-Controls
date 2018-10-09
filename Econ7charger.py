#appologies for poor notes at present will add comments as it all develops
#!/usr/bin/python2.7

import sys
import time as clock
from datetime import datetime
from datetime import time 

from pyModbusTCP.client import ModbusClient
from econ7chargerConf import *

pulse = 0
dpulse = 1
mode = 0
SIUpdated = False
econ7 = False
firstRun = True

def importFromGrid(setPoint, SOCDischarge, SOCCharge):
	log.write('%02d, %02d, %02d, ' %(setPoint, SOCDischarge, SOCCharge))
	#log.write(str(setPoint)+', '+str(SOCDischarge)+', '+str(SOCCharge)+', ')
	hub4 = ModbusClient()
	hub4.host(farmIP)
	hub4.port(hub4Port)
	hub4.unit_id(hub4Id)
	inverter = ModbusClient()
	inverter.host(farmIP)
	inverter.port(invPort)
	inverter.unit_id(invId)
	success = False
	if inverter.open():
		r=inverter.read_input_registers(30,1)
		soc = r[0] / 10.0 # convert to a percentage
		log.write('%.1f, inverter, ' %(soc))
		print 'SOC=', (soc)
	else:
		log.write('failed to open inverter coms')

	#sort the chargeing

	if hub4.open():
		success = True
		if soc < SOCCharge:
			#allow chargeing at max power set point
			log.write('charging, ')
			success = success & hub4.write_single_register(2700, setPoint)
		else:
			#battery sufficiently charged set charging power to 0
			log.write('not charging, ')
			success = success & hub4.write_single_register(2700, 0)

		if soc > SOCDischarge:
			#allow battery to discharge
			log.write('discharging, ')
			success = success & hub4.write_single_register(2702, 100)
		else:
			#disallow discharge
			log.write('not discharging, ')
			success = success & hub4.write_single_register(2702, 0)
		hub4.close()
		log.write('hub4, ')
	else:
		log.write('hub4 failed to open hub4 comms')
	return success

startTime = time(e7StartHr,e7StartMin,0)
endTime = time(e7StopHr,e7StopMin,0)
e7_spans_midnight = e7StartHr*60+e7StartMin > e7StopHr*60+e7StopMin

	
while 1:
	now = datetime.now()
	#print (now)
	year = now.year
	year = year%100
	month = now.month
	day = now.day
	#month = 12
	#day = 1

	lf = '%02d%02dEcon7Log.txt' %(year, month)
	log = open(lf, 'a')
	log.write ('%02d-%02d-%02d, %02d:%02d:%02d, ' %(year, month, day, now.hour, now.minute, now.second))
	
	todaysDate = datetime(now.year,month,day)
	#print 'the date is', (todaysDate),
	winterEndDate = datetime(now.year,lastMonthOfWinter,lastDayOfWinter)
	springEndDate = datetime(now.year,lastMonthOfSpring,lastDayOfSpring)
	summerEndDate = datetime(now.year,lastMonthOfSummer,lastDayOfSummer)
	autumnEndDate = datetime(now.year,lastMonthOfAutumn,lastDayOfAutumn)

	h = now.hour
	m = now.minute
	checkTime = time(h,m,0)

#check economy7
	
	if e7_spans_midnight:
		if checkTime>startTime or checkTime<endTime:
			econ7 = True
	elif checkTime>startTime and checkTime<endTime:#if inside e7 times:
		econ7 = True
	else:
		econ7 = False
	if econ7:
		tariff='night'
	else:
		tariff='day'
	print 'tariff: '+ str(tariff)+'\n',

#find the season
	
	season = 'winter'
	if todaysDate > winterEndDate:
		season = 'spring'
	if todaysDate > springEndDate:
		season = 'summer'
	if todaysDate > summerEndDate:
		season = 'autumn'
	if todaysDate > autumnEndDate:
		season = 'winter'

	print 'season: ', (season)
	log.write(str(season)+', '+str(tariff)+', ')

#do the doings

	if econ7 and (season == 'winter'):
		if day == 13 or day == 27 : 
			importFromGrid(winterSetPoint, 102, 101) # force full charge twice a month
			log.write('full charge, ')
		else:
			importFromGrid(winterSetPoint, winterSOCDischarge, winterSOCCharge)
	elif econ7 and (season == 'spring'):
		if day == 12 or day == 26 : 
			importFromGrid(springSetPoint, 102, 101) # force full charge twice a month
			log.write('full charge, ')
		else:
			importFromGrid(springSetPoint, springSOCDischarge, springSOCCharge)
	elif econ7 and (season == 'summer'):
		importFromGrid(summerSetPoint, summerSOCDischarge, summerSOCCharge)
	elif econ7 and (season == 'autumn'):
		if day == 12 or day == 26 : 
			importFromGrid(autumnSetPoint, 102, 101) # force full charge twice a month
			log.write('full charge, ')
		else:
			importFromGrid(autumnSetPoint, autumnSOCDischarge, autumnSOCCharge)
	else:
		importFromGrid(daySetPoint, daySOCDischarge, daySOCCharge)

	log.write('\n')
	log.close()

#wait time between loops

	clock.sleep(loopInterval)
