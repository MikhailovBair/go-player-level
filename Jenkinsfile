pipeline {
	agent any
	stages {
		stage('Install virtualenv') {
			options {
				timeout(time: 1, unit: 'HOURS')
			}
			steps {
				sh 'python3 -m virtualenv venv -p python3'
				sh '. venv/bin/activate'
				sh 'echo . venv/bin/activate > activate_cmd'
				sh 'cat activate_cmd'
			}
		}
		stage('Install Requirements') {
			steps {
				sh '`cat activate_cmd` && python3 -m pip install -r code/get_blunders/requirements.txt && apt install -y gunicorn && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && apt install -y nodejs && apt install -y npm && npm install -g analyze-sgf && apt install -y libzip-dev && apt-get install -y lsb-core'
			}
		}
		stage('Tester') {
			steps {
				sh '`cat activate_cmd` && cd ./code/get_blunders && PYTHONPATH=. python3 -m pytest --junit-xml report.xml && cd ../../..' 
			}
			post {
				always {
						junit '**/code/get_blunders/report.xml'
					}
			}
		}

	}
}
