# PV Simulator

## Prerequisites

- python and pip
- Pika
- RabbitMQ
- docker

git clone the repo

```shell
git clone https://github.com/tmeftah/pvsim.git
```

change the workdir

```shell
cd pvsim/
```

# Console mode

create virtual environment

```shell
python3 -m venv venv
```

activate the virtual environment

```shell
source venv/bin/activate
```

and install all the dependencies

```shell
pip install -r requirements.txt
```

run rabbitmq docker container first

```shell
docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.9-management
```

than run the following scripts

```python
python meter.py # run the meter
python pvsim.py # run PV simulator
```

after a while you get a **meter.csv** file under **/out** folder.

stop the container

```shell
docker stop rabbitmq
```

<br/><br/>

# Docker compose Mode

you only need to start docker compose

```shell
docker-compose up -d
```

after a while you get a **meter.csv** file under **/out** folder.

you can now stop the containers

```shell
docker-compose down
```

<br/><br/>

# File description

## sunpos.py

calculation of the Solar intensity depending on the geographical postion of the solar panel.

- Solar intensity:
  https://en.wikipedia.org/wiki/Air_mass_(solar_energy)
- Sun Postion: https://levelup.gitconnected.com/python-sun-position-for-solar-energy-and-research-7a4ead801777

## meter.py

it simulate the meter. It sends every second a random value to RabbitMQ with a timestamp.

```python
    {
        "timestamp": now_.strftime("%Y-%m-%d %H:%M:%S"),
        "value": random.randint(0, 9000),
    }
```

in the for loop 86400 is equal to 24h _ 60min _ 60sec.
you can set the sleep value the decrease the frequency of send random meter value.

```python
 for i in range(86400):
            body = json.dumps(
                {
                    "timestamp": now_.strftime("%Y-%m-%d %H:%M:%S"),
                    "value": random.randint(0, 9000),
                }
            )

            self.publish(body, self.queue)
            now_ = now_ + datetime.timedelta(seconds=1)
            time.sleep(0)  # how fast schould send meter value

```

## pvsim.yp

this is the PV Simulator. it lesten to the queue and for each meter value it calculate the sun postion and solar intensity at that timestamp, simulating the power of 1 square meter Panel.

```python
        meter_kW = data["value"]
        timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        self.sunpos.time = timestamp.time()
        self.sunpos.date = timestamp.date()

        # Get the Sun's apparent location in the sky
        azimuth, elevation = self.sunpos.getpos()
```

After calcualting the solar intensity it saves with the meter and the sum of both to a csv file with the help of writer class.

```python
self.writer.addrow([timestamp, meter_kW, solar_intensity, sumpower])

```

# License

This program is licensed under GPL-3.0
