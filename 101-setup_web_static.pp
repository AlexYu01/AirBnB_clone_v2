# Installs and setsup Nginx with puppet
$dirs = [ '/data/', '/data/web_static/',
          '/data/web_static/releases/',
          '/data/web_static/shared/',
          '/data/web_static/releases/test/'
        ]

package { 'nginx':
  ensure  => 'installed',
}

file { $dirs:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755'
}
