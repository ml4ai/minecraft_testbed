package com.asist.asistmod.block;

import com.asist.asistmod.missionhelpers.RoleManager.RoleManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.tile_entity.VictimBlockTileEntity;

import net.minecraft.block.Block;
import net.minecraft.block.material.Material;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;

public class BlockVictim_Saved extends Block {

	// Here we can pass in a reference the Server and the MqttClient
	public BlockVictim_Saved() {
		
		super(Material.GOURD);
		this.setHardness(100f);
		
		//this.onBlockClicked(worldIn, pos, playerIn);
		// TODO Auto-generated constructor stub
	}
	
	@Override public void onBlockClicked(World world, BlockPos pos, EntityPlayer player) {			

		String playerName = player.getName();
		
		System.out.println( "Clicked Safe Block : " + this.getBlockType() );
		
		if ( RoleManager.isPlayerMedic( player.getName() ) ) {
			
			MinecraftServer server = world.getMinecraftServer();				
			
			server.commandManager.executeCommand(server, "tellraw "+playerName+" {\"text\":\"Victim Type : " + this.getBlockType() + ".\",\"color\":\"red\"} " );
			
		}
		
	}
	
	public String getBlockType() {
            
            String thisBlockType = this.getRegistryName().toString();               
            
            String victimType = null;
            
            if( thisBlockType.contentEquals("asistmod:block_victim_saved_a") ){
                victimType = "A";
            }
            else if(thisBlockType.contentEquals("asistmod:block_victim_saved_b")) {
                victimType = "B";
            }
            else if(thisBlockType.contentEquals("asistmod:block_victim_saved_c")) {
                victimType = "C";
            }
            
            return victimType;
        }

}
