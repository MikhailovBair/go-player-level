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
				sh '`cat activate_cmd` && python3 -m pip install -r code/get_blunders/requirements.txt && cp code/get_blunders/katago/.analyze-sgf.yml /home/.analyze-sgf.yml'
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
