# The Pony Express

[![Build Status](https://travis-ci.org/TelekomCloud/pony-express.png)](https://travis-ci.org/TelekomCloud/pony-express.png)

Manage your package landscape. Focuses on getting all packages and versions in your environment and comparing them to upstream repositories. It gives you answer to the questions:

* What applications are installed on what nodes
* What versions are installed where
* Am I running having packaged in my environment? (Compared to upstream or internal repo mirror)

# Running

To run the pony-express server:

    python manage.py runserver

To create and/or migrate the database run:

    python manage.py db migrate

To update the database to the latest state after migrations have been added, run:

    python manage.py db upgrade

# Tests

To run tests:

    python setup.py test

# License

Company: Deutsche Telekom AG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
