#!/usr/bin/env python

from optparse import OptionParser
from os import listdir
from os import remove
from os.path import basename
from os.path import dirname
from os.path import expanduser
from os.path import exists
from os.path import join
from re import search
from subprocess import call

HOME_DIR = expanduser("~")
DOTFILE_DIR = join(HOME_DIR, "dotfiles")
VIM_PLUGIN_DIR = join(DOTFILE_DIR, "vim/bundle")
OHMYZSH_DIR = join(DOTFILE_DIR, "oh-my-zsh")

# Key = filename in dotfiles
# Value = filename to link to in home dir
SYMLINKS = {
    'vimrc': '.vimrc',
    'zshrc': '.zshrc',
    'tmux_conf': '.tmux.conf',
    'tmux_date': '.tmux.date.conf',
    'ackrc': '.ackrc',
    'git-prompt': '.git-prompt.sh',
    'vim': '.vim',
    'oh-my-zsh': '.oh-my-zsh',
}

VIM_PLUGIN_REPOS = [
    "https://github.com/kien/ctrlp.vim.git", # Semantic Analyzer
    "https://github.com/Raimondi/delimitMate.git", # Auto close quotes, parens, etc..
    "https://github.com/Shougo/neocomplete.vim.git", # omnicomplete
    "https://github.com/scrooloose/nerdcommenter.git", # Comment helper
    "https://github.com/scrooloose/nerdtree.git", # File browser
    "https://github.com/ervandew/supertab.git", # Improved tab completion
    "https://github.com/scrooloose/syntastic.git", # Synatx checker
    "https://github.com/majutsushi/tagbar.git", # Ctags side bar
    "https://github.com/bling/vim-airline.git", # PowerLine
    "https://github.com/tpope/vim-fugitive.git", # Git Tools
    "https://github.com/mhinz/vim-signify.git", # VCS diff in sidebar
    "https://github.com/Shougo/vimproc.vim.git", # Interactive commands
    'https://github.com/noahfrederick/vim-noctu.git', # Uses term colors for colorscheme
    "https://github.com/mileszs/ack.vim.git", # Search within directories/files

]

def get_home_path(filename):
    if filename in SYMLINKS.keys():
        filename = SYMLINKS[filename]

    return join(HOME_DIR, filename)

def get_dotfile_path(filename):
    return join(DOTFILE_DIR, filename)

def extract_repo_name_from_url(repo_url):
    return search('.*/(.*)\.git', repo_url).group(1)

def get_user_approval(message):
    choice = raw_input(message)

    if choice.lower() == 'y':
        return True
    elif choice.lower() == 'n':
        return False
    else:
        return get_user_approval(message)

def clean_home_dotfiles(warn=False):
    """
    Remove all dotfiles stored in the home directory and downloaded files in dotfiles.
    """
    approval_request_message = "WARNING: deleting all dotfiles, continue? (Y/N)"
    if warn and not get_user_approval(approval_request_message):
        return False

    print "Cleaning dotfiles..."
    for filename in SYMLINKS.keys():
        home_file = get_home_path(filename)
        if exists(home_file):
            remove(home_file)

    for repo_url in VIM_PLUGIN_REPOS:
        repo_name = extract_repo_name_from_url(repo_url)
        repo_path = join(VIM_PLUGIN_DIR, repo_name)
        if exists(repo_path):
            call(['rm', '-rf', repo_path])

    if exists(OHMYZSH_DIR):
        call(['rm', '-rf', OHMYZSH_DIR])

    return True

def install_dotfiles():
    """
    Download all dependencies to the dotfile folder and symlink the configs
    from the home directory to the dotfile directory.
    """
    print "Installing Oh-My-ZSH..."
    if not exists(OHMYZSH_DIR):
        call(["git", "clone", "http://github.com/robbyrussell/oh-my-zsh.git",
              "--template", OHMYZSH_DIR])

    print "Please remember to 'chsh -s /bin/zsh' and 'source ~/.zshrc'"

    print "Installing Pathogen..."
    pathogen = join(DOTFILE_DIR, "vim/autoload/pathogen")
    call(["curl", "-L", "https://tpo.pe/pathogen.vim", "-o", pathogen])

    print "Setting up Symlinks..."
    for filename in SYMLINKS.keys():
        home_fn = get_home_path(filename)
        dotfile_fn = get_dotfile_path(filename)
        call(["ln", "-sF", dotfile_fn, home_fn])

    print "Cloning Vim plugins..."
    for repo_url in VIM_PLUGIN_REPOS:
        repo_name = extract_repo_name_from_url(repo_url)
        repo_path = join(VIM_PLUGIN_DIR, repo_name)
        call(["git", "clone", repo_url, repo_path])

    print "Installation Complete"

def update_plugins():
    """
    Do a Git Pull on all Vim Plugins to get the latest updates.
    """
    print "Updating Vim Plugins..."
    plugin_paths = listdir(VIM_PLUGIN_DIR)
    for plugin in plugin_paths:
        call(["cd", VIM_PLUGIN_DIR, plugin, ";", "git", "pull", ";"])

    call(['cd', OHMYZSH_DIR, ';', 'git', 'pull', ';'])
    print "Update Complete"

def setup_option_parser():
    """
    Setup the option_parser used to handle the command line arguments.
    """
    parser = OptionParser(usage=("Usage: %s [options] [command]" %
                                 (basename(__file__))),
                          description="MazMachine's Dotfile Manager")
    parser.add_option("-i", "--install",
                      action="store_true",
                      help="Install dotfiles to home directory")
    parser.add_option("-c", "--clean",
                      action="store_true",
                      help="Clean Home Directory Dotfiles")
    parser.add_option("-u", "--update",
                      action="store_true",
                      help="Update plugins")
    return parser

def main():
    option_parser = setup_option_parser()
    options, args = option_parser.parse_args()

    if options.install:
        clean_home_dotfiles(warn=True)
        install_dotfiles()
        update_plugins()
    elif options.clean:
        clean_home_dotfiles()
    elif options.update:
        update_plugins()
    else:
        option_parser.print_help()


if __name__ == '__main__':
    main()
