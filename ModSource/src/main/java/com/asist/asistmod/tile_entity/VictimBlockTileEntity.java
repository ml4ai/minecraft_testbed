package com.asist.asistmod.tile_entity;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.atomic.AtomicReference;

import com.asist.asistmod.block.BlockVictimBase;
import com.asist.asistmod.block.BlockVictim_2;
import com.asist.asistmod.missionhelpers.mapblock.MapBlockManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager;
import com.asist.asistmod.missionhelpers.triage.ClientSideTriageManager.TriageState;
import com.asist.asistmod.network.NetworkHandler;
import com.asist.asistmod.network.messages.MouseInputMessage;
import com.asist.asistmod.network.messages.ParticlesUpdatePacket;
import com.asist.asistmod.network.messages.TriageMessagePacket;

import net.minecraft.block.state.IBlockState;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.DestroyBlockProgress;
import net.minecraft.client.renderer.RenderGlobal;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.nbt.NBTTagCompound;
import net.minecraft.tileentity.TileEntity;
import net.minecraft.util.ITickable;
import net.minecraft.util.ResourceLocation;
import net.minecraft.util.math.BlockPos;
import net.minecraft.world.World;
import net.minecraftforge.fml.common.registry.ForgeRegistries;
import net.minecraftforge.fml.relauncher.ReflectionHelper;

public class VictimBlockTileEntity extends TileEntity implements ITickable  {
	
	RenderGlobal render; 
	
	HashMap<Integer, DestroyBlockProgress> damagedBlocksMap = new HashMap<Integer, DestroyBlockProgress>();
	
	Field damagedBlocks;
	
	String playerName = "Not Set";
	String blockType;
	public Boolean beingHit = false;
	public Boolean hasBroken = false;
	public String triagingPlayer = null;
	
	AtomicReference<TriageState> triageState = new AtomicReference<TriageState>();
	
	int client_ticks = 0;	
	
	
	@Override 
	public void update(){		
		
		// ensures its clientside
		if(this.getWorld().isRemote){					
			
			if(render == null) {
			    render = Minecraft.getMinecraft().renderGlobal;
			}			
			
			if(blockType == null) {
				
				blockType = world.getBlockState(pos).getBlock().getRegistryName().toString();
				
			}
			
			if(damagedBlocks == null) {			
				
				try{					
					  //damagedBlocks = RenderGlobal.class.getDeclaredField("damagedBlocks");
					  damagedBlocks = ReflectionHelper.findField(RenderGlobal.class, "damagedBlocks", "field_72738_E");
					  damagedBlocks.setAccessible(true); 
					  damagedBlocksMap = (HashMap<Integer,DestroyBlockProgress>) damagedBlocks.get(render);
				}
				catch(Exception e) {
					System.out.println("Problem accessing the RenderGlobal_DamagedBlocks field.");
					e.printStackTrace();
				}			
			}
			
			try {				

				
				// AtomicReference lets you alter variable outside of foreach scope
				AtomicReference<Boolean> match = new AtomicReference<Boolean>();
				
				match.set(false);
				
				// could convert values to stream for more efficient filtering ... but we generally only have 1 or 2 damaged blocks in the list 
				damagedBlocksMap.values().forEach(v -> {										
					if( compareBlockPos( v.getPosition() ) ) {
						match.set(true);
						return;
					}
				});
				
				//if ( client_ticks % 20 == 0){
					
				//	System.out.println( "Client Tick : " + this.pos.toString() + " Match : " + match.get() + " BeingHit : " + beingHit);
					
				//}
				
				if ( beingHit ) {					
					
					if( match.get() && (triageState.get() == TriageState.UNSUCCESSFUL || triageState.get() == null) ) {					
						//
							triageState.set(TriageState.IN_PROGRESS);
							//System.out.println(triageState.get());						
							//System.out.println(blockType.length()+","+ blockType+","+ pos.getX()+","+ pos.getY()+","+  pos.getZ()+","+ triageState.get().ordinal()+","+ ClientSideTriageManager.messageId );
							NetworkHandler.sendToServer( new TriageMessagePacket( 
									blockType.length(), blockType, triagingPlayer.length(), triagingPlayer, pos.getX(),pos.getY(), pos.getZ(), triageState.get().ordinal() , ClientSideTriageManager.messageId++ ) );
						
					}					
				}
				
				if( !match.get() && (triageState.get() == TriageState.IN_PROGRESS) ) {
					
					// isVictimBlock() is to check it that the block hasn't been broken/replaced while the tile entity is finishing a damage check loop. If its not a block_victim_1 or 2,
					// that means its been replaced already and obviously will not be in the damaged block array. This was reportedly a bug.
					if( isVictimBlock(this.pos) ) {
					
						triageState.set(TriageState.UNSUCCESSFUL);
						beingHit = false;
						//System.out.println(triageState.get());					
						//System.out.println(blockType.length()+","+ blockType+","+ pos.getX()+","+ pos.getY()+","+  pos.getZ()+","+ triageState.get().ordinal()+","+ ClientSideTriageManager.messageId );
						NetworkHandler.sendToServer( new TriageMessagePacket( 
								blockType.length(),  blockType, triagingPlayer.length(), triagingPlayer, pos.getX(),pos.getY(), pos.getZ(), triageState.get().ordinal() , ClientSideTriageManager.messageId++ ) );
					}
				}		
						
			} catch (IllegalArgumentException e ) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}		
		}		
	}
	
	public boolean compareBlockPos( BlockPos pos) {			
			return ( pos.getX() == this.pos.getX() ) && ( pos.getY() == this.pos.getY() ) && ( pos.getZ() == this.pos.getZ() );
	}
	
	public void updateBlockData( String playerName, String blockType ) {
		this.playerName = playerName;
		this.blockType = blockType;
	}
	
	public boolean isVictimBlock(BlockPos pos) {
		
		String type = world.getBlockState(pos).getBlock().getRegistryName().toString();
		
		return (type.contentEquals("asistmod:block_victim_1") ) || (type.contentEquals("asistmod:block_victim_2"));
	}
	
	
}
