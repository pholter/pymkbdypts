
Parses open boundary information in combination with a given
topography for GETM_ (General Estuarine transport model, www.getm.eu)
setup

.. _GETM: http://www.getm.eu


Install
-------

User
____

Install as a user

.. code:: bash
	  
   python3 setup.py install --user

Uninstall as a user
   
.. code:: bash
	  
   pip3 uninstall pycnv

Developer
_________

Install as a user

.. code:: bash
	  
   python3 setup.py develop --user

Uninstall as a user
   
.. code:: bash
	  
   pip3 uninstall pycnv



USAGE
-----

If you call pymkbdypts in a valid GETM case without further arguments,
pymkbdypts will look for a bdyinfo.dat and a topo.nc and create a
figure showing the bdypoints on that map.

.. code:: bash
	  
   pymkbdypts --figure bdymap.png

If you want to save the bdypoints in a text file call mkbdypts like
this (again in a valid GETM cast with an existing topo.nc and
bdyinfo.dat):

.. code:: bash
	  
   pymkbdypts --output bdypts.txt
	  

If you want to specify different bdyfiles and topo files use the
command lines "--topo" and "--bdyinfo".

Additional to a simple lat,lon list pymkbdypts also offers a output
usable for extracting tides (--format=tides) and an output of convx,
usable to rotate velocities at the boundaries (--format=conv)
