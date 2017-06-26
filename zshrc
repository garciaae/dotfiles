# Path to your oh-my-zsh configuration.
ZSH=~/.oh-my-zsh

# Set name of the theme to load.
# Look in ~/.oh-my-zsh/themes/
# Optionally, if you set this to "random", it'll load a random theme each
# time that oh-my-zsh is loaded.
ZSH_THEME="blinks"

# Set to this to use case-sensitive completion
# CASE_SENSITIVE="true"

# Comment this out to disable bi-weekly auto-update checks
# DISABLE_AUTO_UPDATE="true"

# Uncomment to change how often before auto-updates occur? (in days)
# export UPDATE_ZSH_DAYS=13

# Uncomment following line if you want to disable colors in ls
# DISABLE_LS_COLORS="true"

# Uncomment following line if you want to disable autosetting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment following line if you want to disable command autocorrection
# DISABLE_CORRECTION="true"

# Uncomment following line if you want red dots to be displayed while waiting for completion
 COMPLETION_WAITING_DOTS="true"

# Uncomment following line if you want to disable marking untracked files under
# VCS as dirty. This makes repository status check for large repositories much,
# much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Disable zsh trying to set a title
#DISABLE_AUTO_TITLE="true"

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
plugins=(git git-prompt gitfast git-extras github colorize colored-man common-aliases lol python compleat history mosh osx themes django vim-integration)
source $ZSH/oh-my-zsh.sh
setopt promptsubst

ZSH_THEME_GIT_PROMPT_PREFIX="$fg[white]($fg[red]"
ZSH_THEME_GIT_PROMPT_SUFFIX="$fg[white])"
ZSH_THEME_GIT_PROMPT_CLEAN="$fg[green] *"
ZSH_THEME_GIT_PROMPT_DIRTY="$fg[red] *"
local local_git_prompt='$(git_prompt_info)'

export RPROMPT="%{$fg[white]%}(%{$fg[green]%}%T%{$fg[white]%})%{$reset_color%}"
export PROMPT=" %{$terminfo[bold]$fg[green]%}%n$fg[white]@$fg[white]%m%{$reset_color%}%{$terminfo[bold]$fg[blue]%} $fg[white][$fg[blue]%~$fg[white]] ${local_git_prompt}%{$reset_color%}
%B%{$fg[blue]%}--%{$fg[green]%}> %b%{$reset_color%}"
PROMPT="$PROMPT"'$([ -n "$TMUX" ] && tmux setenv TMUXPWD_$(tmux display -p "#D" | tr -d %) "$PWD")'


export EDITOR=vim VISUAL=vim

alias :q='echo "Silly, this is not vim"'
alias :wq='echo "Silly, this is not vim"'
alias :w='echo "Silly, this is not vim"'
alias gs="git status"
alias gb="git branch"
alias gc="git checkout"
alias gd="git diff"
alias git-clean-branches='git branch --merged | egrep -v "(^\*|master|pubdev|staging|prod)" | xargs git branch -d'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias ag="ack"
alias tmux="tmux -2 -u"
alias vi="vim"

export EDITOR=vim
export VISUAL=vim

export TERM=xterm-256color

[ -f ./.fzf.zsh ] && source ./.fzf.zsh

test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

source ~/.local_profile
