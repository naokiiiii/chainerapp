chainerapp
=====================
## Requiements

- Docker (>=1.6)
- mac os?

## How to use

####Fork & Clone
- https://github.com/(GIT_ID)/chainer.git
- https://github.com/(GIT_ID)/chainerapp.git


####First Setting
ex.
vi ~/.bash_profile
export GIT_HOME=/Users/(UID)/git

####Build DockerImage
  $ ./dockerbin/1_build_chainerapp-test.sh

####Start Container
  $ ./dockerbin/2_run_chainerapp-test.sh

####Stop & Delete Container
  $ ./dockerbin/3_stop_chainerapp-test.sh

####Login Container
  $ ./dockerbin/4_exec_chainerapp-test.sh


####Training on Docker
1. Login Container
  $ ./dockerbin/4_exec_chainerapp-test.sh

2. Prepare training
  docker$ /opt/t4j/chainerapp/dlbin/dl_1_init.sh

3. Train(Generate NN)
  docker$ /opt/t4j/chainerapp/dlbin/dl_2_training.sh
  And you can find NN-models in /var/opt/t4j/chainer-data/model/

4. Inspection
  docker$ /opt/t4j/chainerapp/dlbin/dl_3_inspection.sh some.jpg