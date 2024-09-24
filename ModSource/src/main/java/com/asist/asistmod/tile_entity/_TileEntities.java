package com.asist.asistmod.tile_entity;

import net.minecraftforge.fml.common.registry.GameRegistry;

public final class _TileEntities {

    public static void init() {
        
    	GameRegistry.registerTileEntity(VictimBlockTileEntity.class, "victim_block_tile_entity");
    	
    	GameRegistry.registerTileEntity(VictimBlockProximityTileEntity.class, "victim_block_proximity_tile_entity");
        
    }

}
