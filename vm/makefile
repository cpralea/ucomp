.PHONY: all clean

all: build/vm.so

CXX = g++
CXXFLAGS = -Wall -std=c++17 -g

-include $(patsubst %.cc, build/deps/%.d, $(wildcard *.cc))

build/deps/%.d: %.cc | build/deps
	@$(CXX) $(CXXFLAGS) -E -MMD -MT build/$*.o -MF $@ $< > /dev/null 2>&1

build/%.o: %.cc | build
	$(CXX) $(CXXFLAGS) -c -o $@ $<

build/vm.so: $(patsubst %.cc, build/%.o, $(wildcard *.cc))
	$(CXX) $(CXXFLAGS) -shared -o $@ $^

build:
	mkdir -p $@
build/deps:
	mkdir -p $@

clean:
	rm -rf build
