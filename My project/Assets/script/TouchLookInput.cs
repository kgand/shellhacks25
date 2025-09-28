using UnityEngine;
using UnityEngine.EventSystems;

// 这个脚本需要附加在你创建的透明LookPanel上
public class TouchLookInput : MonoBehaviour, IPointerDownHandler, IPointerUpHandler, IDragHandler
{
    // 公开一个Vector2，让MouseLook脚本可以从中读取滑动增量
    public Vector2 TouchDelta { get; private set; }

    private int currentTouchId = -1; // -1表示当前没有有效触摸

    public void OnPointerDown(PointerEventData eventData)
    {
        // 捕获一个新的触摸，前提是当前没有正在跟踪的触摸
        if (currentTouchId == -1)
        {
            currentTouchId = eventData.pointerId;
            TouchDelta = Vector2.zero; // 开始触摸时重置增量
            Debug.Log ("touch");
        }
    }

    public void OnDrag(PointerEventData eventData)
    {
        // 只有当拖动的触摸是我们正在跟踪的那个触摸时，才更新增量
        if (eventData.pointerId == currentTouchId)
        {
            TouchDelta = eventData.delta; // eventData.delta已经为我们计算好了每帧的滑动增量
            Debug.Log ("move");
        }
    }

    public void OnPointerUp(PointerEventData eventData)
    {
        // 如果抬起的触摸是我们正在跟踪的那个，就停止跟踪
        if (eventData.pointerId == currentTouchId)
        {
            currentTouchId = -1;
            TouchDelta = Vector2.zero; // 触摸结束时重置增量
            Debug.Log ("count");
        }
    }

    // 在禁用时也重置状态，以防万一
    private void OnDisable()
    {
        currentTouchId = -1;
        TouchDelta = Vector2.zero;
    }
}