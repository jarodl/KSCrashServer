KSCrashServer
=============

This is an example server-side API for [KSCrash](http://github.com/kstenerud/KSCrash).

## Set up

	mkvirtualenv ks_crash
	
	# needed for gevent
	brew install libevent
	# needed for juggernaut
	brew install redis

	npm install -g juggernaut

	pip install -r requirements.txt

	gem install foreman

	# start redis
	redis-server

	# start juggernaut
	juggernaut

	# start sonar
	foreman start

## Usage

1. Start redis with `redis-server`
2. Start Juggernaut by running `juggernaut`
3. Run `foreman start`
4. Navigate to [http://localhost:8000/](http://localhost:8000/)
5. Send a few crash reports from the simulator using the included CrashTester app

## API

Right now there are two end points for the API

*Return all reports:*

	/api/reports.json

*Return a single report using the `crash_id`:*

	/api/reports/<crash_id>.json
