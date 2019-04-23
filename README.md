# boxcraft-ironfarm-fix

#### Cardinal direction facing towards:

```
north: -Z
west: -X
south: +Z
east: +X
```

#### Structure of the Iron Farm

- 32 villages (rows of doors in z-direction)
- two banks of 11 doors each (seperated by air)

#### NBT arrangement

- villages sorted by z-coord ascending
- doors of each village are arranged in order of x-coord values:
  - max of upper | min of under (alternating)


#### Links
- [NBT format](https://minecraft.gamepedia.com/NBT_format)
- [Villages.dat format](https://minecraft.gamepedia.com/Villages.dat_format)
- [Python NBT library](https://github.com/twoolie/NBT)
- [Windows NBT Explorer GUI](https://github.com/jaquadro/NBTExplorer)