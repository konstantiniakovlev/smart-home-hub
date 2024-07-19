# Smart-Home-Hub

For some reason, despite setting the environmental variable in ``deploy.yml``:
```
env:
  POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
```
``docker-compose.yml`` is not able to detect it.\
Therefore an additional of line was added:
```echo "POSTGRES_PASSWORD=${{ secrets.POSTGRES_PASSWORD }}" > /home/pi/Projects/smart-home-hub/.env```
to allow for the compose file to be able to read the variable from ``.env`` file.
