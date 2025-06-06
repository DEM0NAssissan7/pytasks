#!/usr/bin/python3

from pytasks import *

# Confirmation Checker
print("WARNING: This script is ONLY tested for Fedora 40. This script WILL break your system if used on any other system.")
print("Type 'Yes' to continue. Otherwise, just press [ENTER]")
i = input("Continue?: ")
if i != "Yes":
    print("Exiting...")
    exit()
needsroot()

prerun("""
    function dnf {
        /usr/bin/dnf -y $@
    }
    function flatpak {
        /usr/bin/flatpak -y $@
    }
    function ask_prompt {
        # Argument 1: Message
        # Argument 2: If yes (function name)
        # 3: If no (function name)
        # 4: Default

        message=$1
        yes=$2
        no=$3

        default=$yes
        p="[Y/n]"

        if [ -z $4 ]; then
            true
        elif [ $4 == "n" ]; then
            default=$no
            p="[y/N]"
        fi


        read -p "$message $p: " input
        if [ -z $input ]; then
            $default
        elif [ ${input,,} == "y" -o ${input,,} == "yes" ]; then
            $yes
        elif [ ${input,,} == "n" -o ${input,,} == "no" ]; then
            $no
        else
            ask_prompt $@
        fi
    }
""")

default_select(True)

Task("Fedora Linux Flathub Removal (repository)",
    "flatpak remote-delete fedora")

Task("GNOME Xwayland fractional scaling (unstable)", """
    dnf copr enable taaem/mutter-xwayland-fractional-scaling

    dnf rei gnome-settings-daemon
    dnf up mutter mutter-common gnome-settings-daemon

    gsettings set org.gnome.mutter experimental-features "['scale-monitor-framebuffer', 'xwayland-native-scaling', 'variable-refresh-rate']"
    """, reboot=True)

Task("Flatpak by Default", """
    gsettings set org.gnome.software packaging-format-preference "['flatpak', 'rpm']"
    killall gnome-software
    """)

Task("Gnome Console (replaces gnome-terminal)", """
    dnf rm gnome-terminal gnome-terminal-nautilus
    dnf in gnome-console
    """)

# This implies that Fedora flatpak repo has already been removed
Task("mpv (app)",
    "flatpak install app/io.mpv.Mpv/x86_64/stable")

Task("Matlab", """
    function matrun {
        toolbox run --container matlab $@
    }
    
    # Shit ton of dependencies
    
    toolbox create matlab --distro rhel --release 8.10
    matrun sudo dnf -y install alsa-lib.x86_64 cairo.x86_64 cairo-gobject.x86_64 cups-libs.x86_64 \
    gdk-pixbuf2.x86_64 glib2.x86_64 glibc.x86_64 glibc-langpack-en.x86_64 glibc-locale-source.x86_64 \
    gtk3.x86_64 libICE.x86_64 libXcomposite.x86_64 libXcursor.x86_64 libXdamage.x86_64 libXfixes.x86_64 \
    libXft.x86_64 libXinerama.x86_64 libXrandr.x86_64 libXt.x86_64 libXtst.x86_64 libXxf86vm.x86_64 \
    libcap.x86_64 libdrm.x86_64 libglvnd-glx.x86_64 libsndfile.x86_64 libtool-ltdl.x86_64 libuuid.x86_64 \
    libwayland-client.x86_64 make.x86_64 mesa-libgbm.x86_64 net-tools.x86_64 nspr.x86_64 nss.x86_64 \
    nss-util.x86_64 pam.x86_64 pango.x86_64 procps-ng.x86_64 sudo.x86_64 unzip.x86_64 which.x86_64 zlib.x86_64
    
    
    
    
    """, selected=False)

Task("Google Chrome",
    "dnf in google-chrome-stable")


run_tasks()