
SOURCES=$(wildcard *.md)
TARGETS=$(SOURCES:%.md=build/%.html)

CSS=https://pipal.in/build/style.min.css

default: $(TARGETS) 
	cp style.css build/

build/%.html: %.md
	@mkdir -p build/
	pandoc -c $(CSS) -c style.css -f markdown -t html5 $< -o $@