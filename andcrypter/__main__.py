import argparse

from .commands import create, mount, umount, android


if __name__ == "__main__":
    # Prepare the main argparser:
    parser = argparse.ArgumentParser(
        prog='andcrypter',
        description='Android Encryption Manager for External Storage',
    )
    subparsers = parser.add_subparsers(
        title='Sub-commands',
        help='Sub-command help:',
    )

    # Sub-command: create
    parser_create = subparsers.add_parser(
        'create',
        help='Create a new encrypted volume in an existing partition',
        description="""
            Creates a new encrypted volume. An existing partition should be provided
            and that will be used as the destination. All the data in the partition
            will be lost.""",
    )
    parser_create.add_argument(
        'dev_path',
        help='Device path (like /etc/dev/sdg3 or '
             '/dev/disk/by-uuid/349f49b1-ab74-4238-bee5-6d74053e231e)',
    )
    parser_create.add_argument(
        'volume_name',
        help='Descriptive (short and unique) name for the volume'
    )

    # Sub-command: mount
    parser_mount = subparsers.add_parser(
        'mount',
        help='Mount an encrypted volume',
        description="""
            Mounts an encrypted volume. First execution must provide the destination
            path, while successive executions will remember the last mount path. This
            will load the encrypted volume (if not loaded yet) and then mount it.""",
    )
    parser_mount.add_argument(
        'volume_name',
        help='Previously defined name for the volume',
    )
    parser_mount.add_argument(
        'mount_path',
        nargs='?',
        help='The destination path for the mount --required only the first time',
    )

    # Sub-command: umount
    parser_umount = subparsers.add_parser(
        'umount',
        help='Unmount an encrypted volume',
        description="""
            Unmounts a previously mounted encrypted volume.""",
    )
    parser_umount.add_argument(
        'target',
        help='Either the volume name or the destination path of the mountpoint'
    )

    # Sub-command: android
    parser_android = subparsers.add_parser(
        'android',
        help='Set up an encrypted volume on an Android device',
        description="""
            Set up an Android device for a certain encrypted volume. Note that adb command
            should be prepared, available and root-ready.""",
    )
    parser_android.add_argument(
        'volume_name',
        help='Previously defined name for the volume',
    )

    args = parser.parse_args()
