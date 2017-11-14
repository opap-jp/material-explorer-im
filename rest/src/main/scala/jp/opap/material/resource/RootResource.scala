package jp.opap.material.resource

import java.io.IOException
import javax.ws.rs.core.{MediaType, Response}
import javax.ws.rs.{GET, Path, Produces}

import com.fasterxml.jackson.databind.ObjectMapper
import jp.opap.material.dao.{MongoItemDao, MongoProjectDao}
import jp.opap.material.facade.{Progress, ProgressListener, ProjectDataEventEmitter}
import org.glassfish.jersey.media.sse.{EventOutput, OutboundEvent, SseFeature}

@Path("")
class RootResource(val projectDao: MongoProjectDao, val itemDao: MongoItemDao, val eventEmitter: ProjectDataEventEmitter) {
  @GET
  @Path("/person")
  @Produces(Array(MediaType.APPLICATION_JSON))
  def person(): Response = {
    val data: Map[String, _] = Map("name" -> "祝園アカネ")
    Response.ok(data).build()
  }

  @GET
  @Path("/repositories")
  @Produces(Array(MediaType.APPLICATION_JSON))
  def repositories(): Response = {
    val items = this.projectDao.findProjects()
    val data = Map("items" -> items)
    Response.ok(data).build()
  }

  @GET
  @Path("/items")
  @Produces(Array(MediaType.APPLICATION_JSON))
  def items(): Response = {
    val items = this.itemDao.findAll()
      .sortBy(item => item.path)
    val data = Map("items" -> items)
    Response.ok(data).build()
  }

  @GET
  @Path("/count")
  @Produces(Array(SseFeature.SERVER_SENT_EVENTS))
  def count(): EventOutput = {
    val eventOutput = new EventOutput()
    new Thread() {
      override def run(): Unit = {
        Iterable.range(0, 1000)
          .foreach(i => {
            val event = new OutboundEvent.Builder()
              .data(i)
              .build()
            Thread.sleep(1)
            eventOutput.write(event)
          })
        eventOutput.close()
      }
    }.start()
    eventOutput
  }

  @GET
  @Path("/progress")
  @Produces(Array(SseFeature.SERVER_SENT_EVENTS))
  def progress(): EventOutput = {
    if (eventEmitter.getRunning) {
      val serialize = (() => {
        val m = new ObjectMapper()
        (o: Object) => m.writeValueAsString(o)
      })()
      val eventOutput = new EventOutput()
      var lastEvent: Long = 0

      eventEmitter.subscribe(new ProgressListener {
        override def onUpdate(progress: Progress): Unit = {
          val event = new OutboundEvent.Builder()
            .data(serialize(progress))
            .build()
          try {
            val current = System.currentTimeMillis()
            val difference = current - lastEvent
            if (difference < 15 || eventOutput.isClosed) {

            } else {
              lastEvent = current
              eventOutput.write(event)
            }
          } catch {
            case e: NullPointerException => {
              System.out.println(e)
            }
            case e: IOException => {
              System.out.println(e)
            }
          }
        }

        override def onFinish(): Unit = {
          val event = new OutboundEvent.Builder()
            .name("close")
            .data("close")
            .build()

          eventOutput.write(event)
          eventOutput.close()
        }
      })
      eventOutput
    } else {
      val event = new OutboundEvent.Builder()
          .name("negative")
          .data("negative")
          .build()
      val eventOutput = new EventOutput()
      eventOutput.write(event)
      eventOutput.close()
      eventOutput
    }
  }
}
