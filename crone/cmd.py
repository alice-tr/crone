
#======================================#
import sys
from datetime import datetime, timedelta, timezone

import inquirer
from inquirer.render.console import ConsoleRender
import pendulum
from flatlib import const, angle
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
#======================================#

from .geopos import GEOPOS_GREENWICH

#======================================#
def getLastFullMoon(chart):
	
	max_error = 0.0003
	
	jd = Datetime.fromJD(chart.date.jd, chart.date.utcoffset).jd
	
	sun  = chart.getObject(const.SUN)
	moon = chart.getObject(const.MOON)
	
	dist = angle.distance(sun.lon, moon.lon)
	
	offset = 180
	
	# placeholder (in case _no_ adjustment made)
	new_chart = chart.copy()
	
	while abs(dist) > max_error:
		
		new_chart = Chart(Datetime.fromJD(jd - (dist / 13.1833), chart.date.utcoffset), chart.pos)
		jd = new_chart.date.jd
		
		sun  = new_chart.getObject(const.SUN)
		moon = new_chart.getObject(const.MOON)
		
		dist = angle.closestdistance(sun.lon - offset, moon.lon)
	
	return Datetime.fromJD(new_chart.date.jd, new_chart.date.utcoffset)


# adapted from : https://stackoverflow.com/a/64837974

def dt_from_jd(jd):
	
	# 1858-11-17
	dt_Offset = 2400000.500
	
	dt = datetime(1858, 11, 17, tzinfo=timezone.utc) + timedelta(jd - dt_Offset)
	
	return dt
#======================================#

#======================================#
def _get_dt_from_text(pos, text):
	
	dt = None
	
	text_lower = text.lower()
	
	if (
		text_lower == 'full moon' or 
		text_lower == 'next full moon' or 
		text_lower == 'at the full moon' or 
		text_lower == 'under the full moon' or 
		# (emoji) Full Moon
		text == '\U0001F315'
	):
		
		# NOTE: _must_ keep in GMT tz here (i.e. NO DST, etc)
		# - then: at the end, can transform back to "user"-time
		
		dt_utc_now = datetime.utcnow()
		
		utc_str_date = dt_utc_now.strftime(r'%Y/%m/%d')
		utc_str_time = dt_utc_now.strftime(r'%H:%M')
		
		date = Datetime(utc_str_date, utc_str_time, '+00:00')
		
		chart_og = Chart(date, pos)
		
		dtime_last_full = getLastFullMoon(chart_og)
		
		# NOW: get a _new_ chart from PAST that, and backtrack again to "full"
		new_dtime = Datetime.fromJD(dtime_last_full.jd + 31, chart_og.date.utcoffset)
		
		chart_past_full = Chart(new_dtime, pos)
		
		next_full = getLastFullMoon(chart_past_full)
		
		dt = dt_from_jd(next_full.jd)
	
	else:
		
		raise Exception(f'could not parse datetime from text : {text}')
	
	return dt
#======================================#

#======================================#
def run_from_docopt(arguments):
	
	#======================================#
	if arguments['foretell'] is True:
		
		cronexp_out = arguments['--cronexp'] is True
		
		#======================================#
		# intialize this here so can potentially share with other operations
		render = ConsoleRender(theme=None)
		
		if (
			arguments['<command>'] is not None and 
			arguments['<timing>'] is not None
		):
			
			command = arguments['<command>']
			timing  = arguments['<timing>']
		
		else:
			
			questions = [
				inquirer.Text('timing', message="Timing"), 
				inquirer.Text('command', message="Command"), 
			]
			
			answers = inquirer.prompt(questions, render=render)
			
			command = answers['command']
			timing  = answers['timing']
		#======================================#
		
		#======================================#
		# now: "command" and "timing" ready for parsing
		
		user_pos = GeoPos(*GEOPOS_GREENWICH)
		
		dt_utc = _get_dt_from_text(user_pos, timing)
		
		# NOTE: explicitly do _not_ zero-pad these values (cron does not necessarily handle gracefully)
		# - however: behavior of embedding this logic into format string (i.e. with '-') is platform-specific, SO just manually handle below
		
		t_minutes = dt_utc.strftime(r'%M')
		t_hours   = dt_utc.strftime(r'%H')
		t_days    = dt_utc.strftime(r'%d')
		t_months  = dt_utc.strftime(r'%m')
		
		if t_minutes.startswith('0'):
			t_minutes = t_minutes[1:]
		if t_hours.startswith('0'):
			t_hours = t_hours[1:]
		if t_days.startswith('0'):
			t_days = t_days[1:]
		if t_months.startswith('0'):
			t_months = t_months[1:]
		
		str_cronexp = f'{t_minutes} {t_hours} {t_days} {t_months} * {command}'
		
		if cronexp_out:
			
			#sys.stdout.write(str_cronexp)
			# NOTE: "print" here so no confusion about END of cron line (would be not good b/c its a literal command)
			print(str_cronexp)
			
		else:
			
			# NOTE: use terminal already established for inquirer
			term = render.terminal
			
			str_natlang = pendulum.instance(dt_utc).diff_for_humans(locale='en')
			str_date = dt_utc.strftime(r'%H:%M on %m-%d-%y, UTC+00:00')
			
			print(f'{term.cyan}\n{timing}{term.normal} ,\n{term.orange}   {command}')
			print('')
			print(f'{term.green}    Next Chance: {term.normal}{str_natlang} ({str_date})')
			print(f'{term.magenta}CRON Expression: {term.normal}{str_cronexp}')
			print('')
			
		#======================================#
		
	else:
		
		raise Exception(f'unrecognized command')
	#======================================#
	
	return
#======================================#
