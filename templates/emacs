(require 'package)

(add-to-list 'package-archives '("org" . "http://orgmode.org/elpa/"))
(add-to-list 'package-archives '("melpa" . "http://melpa.org/packages/"))
(add-to-list 'package-archives '("melpa-stable" . "http://stable.melpa.org/packages/"))

(setq package-enable-at-startup nil)

(defun ensure-package-installed (&rest packages)
  "Assure every package is installed, ask for installation if it’s not.

Return a list of installed packages or nil for every skipped package."
  (mapcar
   (lambda (package)
     (if (package-installed-p package)
         nil
       (if (y-or-n-p (format "Package %s is missing. Install it? " package))
           (package-install package)
         package)))
   packages))

;; Make sure to have downloaded archive description.
(or (file-exists-p package-user-dir)
    (package-refresh-contents))

;; Activate installed packages
(package-initialize)

;; Assuming you wish to install "iedit" and "magit"
(ensure-package-installed 'iedit 'magit 'evil 'helm 'slime)
(require 'evil)
(evil-mode 1)
(global-set-key (kbd "C-z") 'keyboard-quit)

(require 'helm-config)
(helm-mode 1)

(add-to-list 'load-path ".emacs.d/elpa/slime-20160907.602/")
(setq inferior-lisp-program "/usr/bin/clisp")
(require 'slime-autoloads)
(slime-setup '(slime-fancy))
