# netdata_tegrastats
This plugin inspired from nvidia-smi plugin.
Add Nvidia Jetson Xavier GPU to netdata dashboard

# How to install
1. Copy tegrastat.chart.py file to the python.d location (`/usr/libexec/netdata/python.d`)
2. Copy tegrastat.conf file to `/etc/netdata/python.d/` location.
3. Edit python.d.conf file ( located at `/usr/lib/netdata/conf.d/python.d.conf`) and add `tegrastat: yes` under nvidia-smi
4. Restart your netdata ( `systemctl restart netdata` )

Things to do:
- [ ] Check fan RPM - For now the file want root permissons
- [ ] Add gpu usage gauge to dashboard_info.js
