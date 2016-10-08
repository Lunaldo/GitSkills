/etc/serf/setup.py:
  file.managed:
    - source: salt://cdn/soft/shaque2/serf/setup.py
    - mode: 755

set_up_serf:
  cmd.run:
    - cwd: /etc/serf
    - name: ./setup.py &>/dev/null
