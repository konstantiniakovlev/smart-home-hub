# Smart-Home-Hub

## Run Locally
1. Set correct ``POSTGRES_PASSWORD`` env variable in either ``.env`` file
or project configurations in your IDE.
2. Run local build make command: 
```bash
make run-local
```

## Run in Docker
1.  Set correct ``POSTGRES_PASSWORD`` env variable in either ``.env`` file 
or current virtual environment.
2. Build and run all docker images using make command:
```bash
make build-all
```

## Setting up self-hosted runner on Raspberry Pi
Instructions on how to set up a self-hosted runner can be found
on GitHub documentation page: 
[link](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners). 

Using self-hosted runners in a workflow: [link](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/using-self-hosted-runners-in-a-workflow).

The self-hosted runner must be set up as a service using ``svc.sh`` script: [link](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/configuring-the-self-hosted-runner-application-as-a-service).

## Custom Domain
To utilize the custom domain set in ``nginx/nginx.conf``,
add the following line to ``/etc/hosts`` on Raspberry Pi:

```
127.0.1.1 home-hub.local
```

## Notes
For some reason, despite setting the environmental variable in ``deploy.yml``:
```
env:
  POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
```
the ``docker-compose.yml`` file is not able to detect it.\
Therefore an additional line was added:
```echo "POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}" > /home/pi/Projects/smart-home-hub/.env```
to allow for the compose file to be able to read the variable from ``.env`` file.
