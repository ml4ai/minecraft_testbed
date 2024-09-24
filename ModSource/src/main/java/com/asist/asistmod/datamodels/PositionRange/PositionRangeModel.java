package com.asist.asistmod.datamodels.PositionRange;

import net.minecraft.util.math.BlockPos;

public class PositionRangeModel {

    public String commandLineOut;

    private int fromX;
    private int fromY;
    private int fromZ;
    private int toX;
    private int toY;
    private int toZ;

    public BlockPos from;
    public BlockPos to;

    public PositionRangeModel(int fromX, int fromY, int fromZ, int toX, int toY, int toZ) {
        this.fromX = fromX;
        this.fromY = fromY;
        this.fromZ = fromZ;
        this.toX = toX;
        this.toY = toY;
        this.toZ = toZ;

        this.from = new BlockPos( this.fromX, this.fromY, this.fromZ );
        this.to = new BlockPos ( this.toX, this.toY, this.toZ );
        this.commandLineOut = this.fromX + " " + this.fromY + " " + this.fromZ + " " + this.toX + " " + this.toY + " " + this.toZ;
    }

    public PositionRangeModel(String rangeStr) {
        String[] coords = rangeStr.trim().split("\\s+");
        if (coords.length == 6 || coords.length == 7) {
            this.fromX = Integer.parseInt(coords[0]);
            this.fromY = Integer.parseInt(coords[1]);
            this.fromZ = Integer.parseInt(coords[2]);

            this.toX = Integer.parseInt(coords[3]);
            this.toY = Integer.parseInt(coords[4]);
            this.toZ = Integer.parseInt(coords[5]);

            this.from = new BlockPos( this.fromX, this.fromY, this.fromZ );
            this.to = new BlockPos ( this.toX, this.toY, this.toZ );
            this.commandLineOut = this.fromX + " " + this.fromY + " " + this.fromZ + " " + this.toX + " " + this.toY + " " + this.toZ;
        }
    }
    public String getString() {
        return commandLineOut;
    }
}
