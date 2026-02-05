# Custom Ubuntu 24.04 ISO (live + install)

This folder contains a live-build setup for a customized Ubuntu 24.04 (GNOME) ISO.

## Prereqs (Ubuntu host)

```bash
sudo apt-get update
sudo apt-get install -y live-build debootstrap squashfs-tools xorriso \
  grub-pc-bin grub-efi-amd64-bin mtools
```

## Build

```bash
cd /workspaces/lucid-empire-linux/scripts
sudo USER_NAME=custom USER_PASSWORD=changeme ./build-ubuntu-iso.sh
```

The ISO is created in the `iso` directory. The default name is typically
`live-image-amd64.hybrid.iso`.

## Customize

- Packages: edit `config/package-lists/custom.list.chroot`
- Sysctl: edit `config/includes.chroot/etc/sysctl.d/99-custom.conf`
- Services: edit `config/hooks/live/020-services.hook.chroot`
- User: edit `config/hooks/live/030-user.hook.chroot` or pass `USER_NAME` and
  `USER_PASSWORD` env vars at build time
- GNOME defaults: edit `config/includes.chroot/etc/dconf/db/local.d/00-custom`

## Notes

- This build uses live-build. It produces a live ISO with an installer.
- If you need unattended installs, we can add an autoinstall config next.
