#### Setting up Project:
##### Setting up ApplicationLayer:

```sh
    $ cd ApplicationLayer
    $ ./setup.sh
```

##### Production mode:

**After following setting up requirements**
```sh
    $ supervisord -c supervisord.conf
```

##### Debugging:

```sh
    $ supervisorctl
```
*Commands*  - `status, restart all, stop all, start all etc`

##### To start in development mode:

```sh
    $ python server.py
```

##### Uninstalling ApplicationLayer:

```sh
    $ cd ApplicationLayer
    $ ./uninstall.sh
```
