# Android Encryption Manager for External Storage

This tool, called `andcrypter`, is aimed to use the adopted storage (which is, in
principle, associated to a one and only physical device) from Linux and/or several
devices. The main idea is to have a "quite secure" pendrive that can be used from
Linux distributions in addition to be connected (and understood) by more than one
Android device (like a phone and a tablet).

## Preflight check

In order to use this project you need:

  * **Linux** You will need `sudo` in order to install and use `dmsetup`.
  * **Python 3** Included by almost all up-to-date Linux distributions.
  * **Rooted Android 5.0 device** You will need Marshmallow or newer in order to use
  the adopted storage and ecryption features, and you need root in order to change
  the encryption key of the partitions).

Remember that there are a couple of steps that are dangerous and you may lose a
partition, and thus your data. Some commands require superuser permissions on your
Linux, and it is easy to mess up. Also, you need `root` access to your Android device,
which is also dangerous if used without knowledge.

## Disclaimer

This is Work In Progress, and the software is provided as-is. If you don't understand what this
software does, you may lose data. A lot of data. So be sure to know what you are doing.

I am not responsible of any of your actions (and don't complain if bad things happen). If you detect a bug
please submit an issue and comment your problem.

## Usage of the `andcrypter` tool

### Disk preparation

First of all, prepare the pendrive. You may want to add some partition (for example,
Android by default uses `gpt` partition table and puts a small FAT32 partition as
the first partition). You may want to have a FAT32 partition + the encrypted one
at the end. Use whatever tool you are comfortable with, `gparted` is a great
graphical choice but you can also use `fdisk` if you are comfortable at a lower level.

Take care on what partition is the one that will be encrypted. All the data in that
partition will be lost. The partition path (`/dev/sdX#`, like `/dev/sdf2`) may change.

This path will be used once.

### Partition creation

The following command will prepare the partition:

    andcrypter create /dev/sdX# <friendly_name>

**DANGEROUS: If you put an invalid path, all the data in that partition will be lost**

What this command does is format the partition and store it internally as the
"`<friendly_name>` partition". Use a unique descriptive short name.

Encryption-wise, this command will generate a random key and ask for a passphrase
in order to secure the key. The passphrase alone is *not* enough in order to decrypt
the disk. You need to extract the encryption key (using the subcommand `export`).

### Mount the partition

The partition will be mounted with the command:

    andcrypter mount <friendly_name> [<path>]

If the encrypted partition is not "loaded", this command will load it (first asking
the passphrase) and then will `mount` it. Note that both commands require superuser
permissions and thus `andcrypter` will perform the command through `sudo`.

The parameter `<path>` is required in the first execution. On successive executions,
the path is remembered and is not required.

### Umount the partition

The command to umount a mounted partition is:

    andcrypter umount <friendly_name>|<path>

This subcommand accepts *either* the "short name" or the path in which it is
mounted. It performs (almost transparently) a `sudo umount`.

### Prepare the Android device

The command `adb` should be available and ready for `root` action. That means that
you should (previously) connected your phone and allowed android debugging and
superuser access. The different mechanisms are outside the scope of this document.

This tool prepares the Android for the already-created encrypted partition through
the subcommand `android`

    andcrypter android <friendly_name>

This command will ask the passphrase and proceed to put the encryption key into
the Android device. Once this is done, Android will recognize the partition as
"adopted storage" and use it accordingly.

Android will mount automatically the partition as soon as you connect it. To
unmount or simply to remove it entirely from the Android, go to Settings > Storage.
There you will be able to "Forget" the device (it will remove the encryption key
from the device) or "Eject" it (do it before unplugging the USB, otherwise you
may end up with a corrupt partition and lose your encrypted data).

## Other sources of information

The official documentation has the standard **Encryption** page available at
https://source.android.com/security/encryption/

A lot of nice insight on the Marshmallow encryption stuff available here:
http://nelenkov.blogspot.com.es/2015/06/decrypting-android-m-adopted-storage.html
Although it may be a bit ouf of date (and reverse engineers things that now should be open)
I understood the mechanisms thanks to that blog entry, so, credit were is due.
