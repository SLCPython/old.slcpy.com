slcpy.com
=========

Official Repo of SLCPython's website

[twitter](https://twitter.com/slcpy)
[meetup](www.meetup.com/Salt-Lake-City-Python-Web-Developers/)

## Contributing

### Fork & Clone the Repo

1. `git clone git@github.com:<your github username>/slcpy.com`
2. `cd slcpy`

### Local Dev Set up

Install virtualenv & virtualenvwrapper

Activate virtualenvwrapper

`mkvirtualenv slcpy`

Add localsettings to virtualenv:

In `~/.virtualenvs/slcpy/bin/postactivate` add this line →`export DJANGO_SETTINGS_MODULE=slcpy.settings.local`

Add apps to your virtualenv:

    add2virtualenv `pwd`/apps # note the backticks

Deactivate and reactivate virtualenv in the slcpy folder:

`deactivate && workonslcpy`

### Pull requests

When you've finished your coding, create a new git branch, commit to that branch, and merge to `master`. We use [nvie's succesful git branching model](nvie.com/posts/a-successful-git-branching-model/) for managing branches.

Push your master branch to your repo and send a pull request. See below for directions on pushing straight to production.

### Handy tips

Adding the following to your `.bash_aliases`, `.bashrc` or `.bash_profile` will let you easily set up a dev environment:

    alias slcpy='cd ~/<your workspace folder>/slcpy && workon slcpy`
    alias startslcpy='slcpy && ./manage.py runserver`
    
### Coding Best Practices

* **Do not use tabs to indent**. Use *spaces* for all indentation.
* `html`,`css`,`sass/scss`, and `javascript` files should only have **2 space indents**
* `python` files should have **4 space indent**
* `png` is the preferred image format.
* With images, if no automatic conversion is available, use the following imagemagick/graphicsmagick command: `gm convert <image>.jpg -resize 960x -unsharp 2x0.5+0.7+0 -quality 98 <image>.png`

## Production deployment

### Public key

Contact `faris [ät] theluckybead.com` or send a pull request to get your public key placed in the production repo.

### Pushing to prod

Once your public key is added to the repo, add the production repo to your remote as follows:

    git remote add production git@slcpy.com:slcpy.com.git

Then you can push to the repo via:

    git push origin master && git push production master
    
The app server will reboot and run `collectstatic -l` to link up static files.
