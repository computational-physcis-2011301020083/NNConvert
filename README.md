How to Xbb to lwtnn configuration
=================================

We can't run Keras directly in ATLAS code. Instead we use some scrips
in [lwtnn][1] to convert the saved NN to a json format, which we can
read from ATLAS code to initialize the network. The network is then
run in lwtnn code within Athena.

To convert a Keras model into something you can run in Athena, you'll
have to add some information specifying the names of the inputs and
outputs. Then you have to convert to the lwtnn json format. This code
is supposed to walk you through that process.


Creating the input specification
--------------------------------

I added a script called `build-spec.py` to make the variable
specification from wei's saved mean and standard deviation
files. There was some guesswork trying to align the indices for the
variables here, so it's possible there were some bugs.

To use this script, run

```python
./build-spec.py meanstd.h5 > variable-spec.json
```

This should give you a json file which specifies the inputs for each
part of the NN, together with the offset and scale values.

Note that when inputs are fed to the NN, they are transformed as

```
y = (x + offset) * scale
```

. This usually means that
```
offset = -mean
scale = 1 / stddev
```

I'm assuming this is true in the `./build-spec.py` script.


Creating the lwtnn input
------------------------

If you've cloned lwtnn, you should be able to run

```
path/to/lwtnn/converters/kerasfunc2json.py WeiAdmStd_JKDL1r_architecture.json WeiAdmStd_JKDL1r_weights.h5 variable-spec.json > network.json
```

This should produce a network which is identical to the [one we put in
the `/dev` area][2]. If it's not the same that's a hint that something
might be weird, but I checked this and they look identical.


Testing the network
-------------------

Even if we produce exactly the same network as before, it's possible
we're just doing the conversion wrong (i.e. the input specification
might be incorrect).

The easiest way to test the network is to run a pattern through lwtnn
and see if it gives the same output that we'd expect from the keras
network. You can either set up an ATLAS release or build lwtnn
yourself, either way you can run

```
lwtnn-test-lightweight-graph network.json inputs.json
```

Where `inputs.json` is the inputs you want to test. This should print
some output values. These need to be checked against what we're
getting from Wei's model. I wrote a dummy version of this file in this
package, but you're free to change the values so they match whatever
inputs are being given in Keras.

[1]: https://github.com/lwtnn/lwtnn
[2]: https://atlas-groupdata.web.cern.ch/atlas-groupdata/dev/BTagging/2020v2/Xbb/GhostVR30Rmax4Rmin02TrackJet_BTagging201903/network.json
