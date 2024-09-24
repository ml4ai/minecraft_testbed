package com.asist.asistmod.block;

import java.util.Random;

import com.asist.asistmod.missionhelpers.RoleManager.RoleManager;
import com.asist.asistmod.missionhelpers.Scoreboard.ScoreboardManager;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.pause.PauseManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.missionhelpers.victims.VictimLocations;
import com.asist.asistmod.missionhelpers.victims.VictimsSavedManager;
import com.asist.asistmod.mqtt.InternalMqttClient;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MissionTimerPacket;
import com.asist.asistmod.network.messages.TeamScoreUpdatePacket;
import com.asist.asistmod.network.messages.TriageMessagePacket;
import com.asist.asistmod.network.messages.VictimCountUpdatePacket;
import com.asist.asistmod.tile_entity.VictimBlockTileEntity;

import net.minecraft.block.Block;
import net.minecraft.block.BlockContainer;
import net.minecraft.block.material.Material;
import net.minecraft.block.state.IBlockState;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.server.MinecraftServer;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.EnumBlockRenderType;
import net.minecraft.util.EnumParticleTypes;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import net.minecraftforge.fml.relauncher.Side;
import net.minecraftforge.fml.relauncher.SideOnly;

public class BlockVictimBase extends BlockContainer {				

		public BlockVictimBase() {
		   
	        super(Material.WOOD);	    
			this.setTickRandomly(true);	
			
		}
		
		// MAKES THE RENDERER WORK, OTHERWISE BLOCK IS INVISIBLE
		@Override
		public EnumBlockRenderType getRenderType( IBlockState state) {
		  return EnumBlockRenderType.MODEL;
		}
		
		// DONT DROP ANY ITEMS
		@Override public int quantityDropped(Random par1Random){ return 0;}
		
		@Override public void onBlockClicked(World world, BlockPos pos, EntityPlayer player) {			
			
			// tell the tile entity that this is the block we are hitting, with this Player --> so triage updates only go for this block
			// this property needs to be updated on both Server and Client
			String playerName = player.getName();
			VictimBlockTileEntity te = (VictimBlockTileEntity)(world.getTileEntity(pos));
			te.beingHit =  true;
			te.triagingPlayer = playerName;
			
			if ( RoleManager.isPlayerMedic( player.getName() ) ) {
				
				MinecraftServer server = world.getMinecraftServer();				
				
				server.commandManager.executeCommand(server, "tellraw "+playerName+" {\"text\":\"Victim Type : " + this.getBlockType() + ".\",\"color\":\"red\"} " );
				
			}
			
		}
		
		@Override public void onBlockDestroyedByPlayer(World world, BlockPos pos, IBlockState blockState) {				
			
			world.removeTileEntity(pos);
			
			String thisType = this.getBlockType();
			String placeType = null;
			
			
			if(thisType.contentEquals("A")) { 
				
				placeType = "block_victim_saved_a";	
				
			}
			else if(thisType.contentEquals("B")) { 
				
				placeType = "block_victim_saved_b"; 			
			
			}
			else if(thisType.contentEquals("C")) { 
				
				placeType = "block_victim_saved_c";       			
			
			}
			
			IBlockState safeblock = ForgeRegistries.BLOCKS.getValue(new ResourceLocation("asistmod", placeType)).getDefaultState();			
			
			world.setBlockState(pos, safeblock);		
		
		}
		
		@Override
		public TileEntity createNewTileEntity(World worldIn, int meta) {
			
			VictimBlockTileEntity tileEntity = new VictimBlockTileEntity();
			
			return tileEntity;
		}
		
		@Override public void updateTick(World worldIn, BlockPos pos, IBlockState state, Random random) {
			//System.out.println("Normal Tick Update?" );
		}
		
		@Override public void randomTick(World worldIn, BlockPos pos, IBlockState state, Random random) {
			//System.out.println("Random Tick Update! : " + pos.toString() );
		}
		
		@Override public int tickRate(World worldIn) {
			return 1;
		}
		
		public String getBlockType() {
			
			String thisBlockType = this.getRegistryName().toString();				
			
			String victimType = null;
			
			if( thisBlockType.contentEquals("asistmod:block_victim_1") ){
				victimType = "A";
			}
			else if(thisBlockType.contentEquals("asistmod:block_victim_1b")) {
				victimType = "B";
			}
			else if(thisBlockType.contentEquals("asistmod:block_victim_2")) {
				victimType = "C";
			}
			
			return victimType;
		}

		
		
}
