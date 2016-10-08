/etc/serf:
  file.directory:
    - user: root
    - group: root
    - dir_mode: 755

stop_serf:
  service.dead:
    - name: serf

serf_archive:
  archive.extracted:
    - name: /usr/local/bin/
    - source: https://cdn.pkg.xmaster.i.qingcdn.com/cdn/soft/shaque/serf.zip
    - source_hash: https://cdn.pkg.xmaster.i.qingcdn.com/cdn/soft/shaque/serf.md5
    - archive_format: zip
    - if_missing: /usr/local/bin/tmp

/usr/local/bin/serf:
  file.managed:
    - mode: 755

/etc/logrotate.d/serf:
  file.managed:
    - source: salt://cdn/soft/shaque2/serf/serf_log.conf

/etc/serf/setup.py:
  file.managed:
    - source: salt://cdn/soft/shaque2/serf/setup.py
    - mode: 755

/etc/init.d/serf:
  file.managed:
    - source: salt://cdn/soft/shaque2/serf/serf.sh
    - mode: 755

set_up_serf:
  cmd.run:
    - cwd: /etc/serf
    - name: ./setup.py agent 7950 7380 172.18.15.2 &>/dev/null
