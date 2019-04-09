# Installs and setsup Nginx with puppet
$dirs = [ '/data/', '/data/web_static/',
          '/data/web_static/releases/',
          '/data/web_static/shared/',
          '/data/web_static/releases/test/'
        ]
exec { 'install stdlib':
  command => 'puppet module install --force puppetlabs-stdlib',
  path    => ['/usr/bin', '/usr/sbin'],
}->
exec { 'update':
  command => 'sudo apt-get update',
  path    => ['/usr/bin', '/usr/sbin'],
}->
exec { 'install nginx':
  command => 'sudo apt-get install -y nginx',
  path    => ['/usr/bin', '/usr/sbin'],
}->
file { $dirs:
  ensure => directory,
  mode   => '0755'
}->
file { '/data/web_static/releases/test/index.html':
  ensure  => present,
  content => 'Hello world',
}->
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
}->
exec { 'check file':
  command => 'sudo echo "http {\n}" > /etc/nginx/nginx.conf',
  onlyif  => 'test -e /etc/nginx/nginx.conf',
  creates => '/etc/nginx/nginx.conf',
  path    => ['/usr/bin', '/usr/sbin'],
}->
file { '/etc/nginx/nginx.conf':
  ensure => present,
}->
file_line { 'Append':
  path  => '/etc/nginx/nginx.conf',
  line  => "http {\n\tserver {\n\t\tlisten 80;
\t\tlocation /hbnb_static {\n\t\t\talias /data/web_static/current/;\n\t\t}
\t}",
  match => '^http {$',
}->
file_line { 'comment out':
  path  => '/etc/nginx/nginx.conf',
  line  => "\t#include /etc/nginx/sites-enabled/*;",
  match => "^\tinclude /etc/nginx/sites-enabled/\\*;$",
}->
exec { 'restart nginx':
  command => 'sudo service nginx restart',
  path    => ['/usr/bin', '/usr/sbin'],
}
