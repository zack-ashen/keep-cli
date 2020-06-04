# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# Maintainer: Your Name <youremail@domain.com>
pkgname=keep-cli-git
pkgver=89.5007a47
pkgrel=1
epoch=
pkgdesc="Keep-cli is a cli Google Keep client. You can add, delete, and manage your Google Keep notes."
arch=('any')
url="https://github.com/zack-ashen/keep-cli"
license=('MIT')
depends=('python')
makedepends=('python-setuptools' 'git')
provides=('keep-cli')
conflicts=('keep-cli')
source=('git://github.com/zack-ashen/keep-cli.git')
md5sums=('SKIP')

_gitname="keep-cli"

pkgver() {
  cd $_gitname
  echo $(git rev-list --count HEAD).$(git rev-parse --short HEAD)
}

package() {
	msg "Running setup.py"
  	python setup.py install --root=${pkgdir} --prefix=/usr
}
