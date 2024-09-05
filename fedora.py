from tasks import *

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

Task("Fedora Linux Flathub Removal (repository)",
     "flatpak remote-delete fedora", selected=True)

Task("Flatpak by Default", """
    gsettings set org.gnome.software packaging-format-preference "['flatpak', 'rpm']"
    killall gnome-software
    """, selected=True)

Task("Gnome Console (replaces gnome-terminal)", """
    dnf rm gnome-terminal gnome-terminal-nautilus
    dnf in gnome-console
    """, selected=True, reboot=True)

# This implies that Fedora flatpak repo has already been removed
Task("mpv (app)",
     "flatpak install app/io.mpv.Mpv/x86_64/stable", selected=True)


run_tasks()