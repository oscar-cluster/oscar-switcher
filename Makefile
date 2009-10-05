PKGDEST=/tmp

deb: clean
	/usr/bin/build_package --type deb --output $(PKGDEST) --url http://www.csm.ornl.gov/srt/downloads/oscar/env-switcher-1.0.13.tar.gz --package-name env-switcher --verbose

rpm: clean
	/usr/bin/build_package --type rpm --output $(PKGDEST) --url http://www.csm.ornl.gov/srt/downloads/oscar/env-switcher-1.0.13.tar.gz --package-name env-switcher --verbose

clean:
