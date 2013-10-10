DEV=NO
TEST=NO

ifeq ($(TEST),YES)
    SETTINGS = possum/settings.py-test
endif
ifeq ($(DEV),YES)
    SETTINGS = possum/settings.py-dev
endif
ifeq ($(DEV),NO)
  ifeq ($(TEST),NO)
    SETTINGS = possum/settings.py-sample
  endif
endif

all: doc

doc:
	cd doc && make html

uml:
	tools/uml.py
	
launch:
	python manage.py settings=${SETTINGS}

test:
	python manage.py test settings=${SETTINGS}
	
model:
	./manage.py graph_models --output=doc/images/models-base.png -g base

