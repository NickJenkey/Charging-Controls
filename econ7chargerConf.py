# Change these to suit installation

farmIP = "192.168.1.10" # IP address of CCGX Modbus TCP interface
e7StartHr = 01 # Economy 7 start hour (in 24hr notation)
e7StartMin = 10 # Economy 7 start mins (in 24hr notation)
e7StopHr = 07 # Economy 7 end hour (in 24hr notation)
e7StopMin = 50 #Economy 7 end mins
# Change these if you want to be chased by an angry man with a big stick
hub4Port = 502 #standard for modbus
hub4Id = 100 #consult hardware documentation for this number this is in the XLS sheetand victron documentation
invPort = 502
invId = 246 #first id on list in xls sheet
meterPort = 502
meterId = 247

#this program was written for a system based in Wales UK and assumes northern hemisphere use.
#it will not set the season properly in the southern hemisphere where the year boundry is not in the winter.

#[season]SetPoint - Max power to draw from grid on economy7 in watts -ve numbers dont seem to work
#[season]SOCDischarge = xx% - dischage threshold, allow battery to discarge during economy7 if SOC above this value in %
#[season]SOCCharge = yy% - charge threshold , charge battery during economy7 if SOC bellow this value in %

lastMonthOfWinter = 2
lastDayOfWinter = 28
winterSetPoint = 10000
winterSOCDischarge = 80
winterSOCCharge = 90 

lastMonthOfSpring = 3
lastDayOfSpring = 31
springSetPoint = 6000
springSOCDischarge = 50
springSOCCharge = 40

lastMonthOfSummer = 8
lastDayOfSummer = 31
summerSetPoint = 5000
summerSOCDischarge = 35
summerSOCCharge = 31

lastMonthOfAutumn = 9
lastDayOfAutumn	= 30
autumnSetPoint = 6000
autumnSOCDischarge = 85
autumnSOCCharge = 45

daySetPoint = 0
daySOCDischarge = 30
daySOCCharge = 0

logPath = '/home/energy/econ7charger/' # path to directory where log files will be written, include trailing /
loopInterval = 300 #how often to update victron in seconds, probably should be about 600 (- 10 minutes)
