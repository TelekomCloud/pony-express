Make sure you have your GPG key in launchpad + verified
Make sure that key is on the machine you're running this

```bash
VERSION="0.7.3"

rm -rf package-build && mkdir package-build && cd package-build
git clone https://github.com/TelekomCloud/pony-express.git

cd pony-express
git checkout <VERSION>
git tag debian/$VERSION-1
uscan --force-download
debuild -S -sa
cd ..

dput ppa:telekomcloud/pony-express ponyexpress_$VERSION-1_source.changes
```
