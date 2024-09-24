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

public class BlockMarkerBase extends BlockContainer {				

		public BlockMarkerBase() {
		   
	        super(Material.WOOD);	
	        
			
		}
		
		// MAKES THE RENDERER WORK, OTHERWISE BLOCK IS INVISIBLE
		@Override
		public EnumBlockRenderType getRenderType( IBlockState state) {
		  return EnumBlockRenderType.MODEL;
		}

		@Override
		public TileEntity createNewTileEntity(World worldIn, int meta) {
			// TODO Auto-generated method stub
			return null;
		}		
}
