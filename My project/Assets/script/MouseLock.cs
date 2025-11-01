// using UnityEngine;

// public class MouseLook : MonoBehaviour
// {
//     // --- 单例模式 ---
//     // 创建一个静态实例，让其他任何脚本都能轻松访问到这个MouseLook脚本
//     public static MouseLook Instance { get; private set; }

//     [SerializeField] private float mouseSensitivity = 100f;
//     [SerializeField] private Transform playerBody;

//     private float xRotation = 0f;
//     private bool isCursorLocked = true; // 增加一个状态变量来跟踪鼠标是否被锁定

//     // Awake在Start之前执行，用于初始化
//     private void Awake()
//     {
//         // 设置单例实例
//         if (Instance == null)
//         {
//             Instance = this;
//         }
//         else
//         {
//             Destroy(gameObject);
//         }
//     }

//     void Start()
//     {
//         // 初始时锁定鼠标
//         LockCursor();
//     }

//     void Update()
//     {
//         // 只有当鼠标被锁定时，才允许转动视角
//         if (!isCursorLocked)
//         {
//             return; // 如果鼠标没锁定，直接跳出Update，不执行下面的代码
//         }

//         // 获取鼠标输入
//         float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity * Time.deltaTime;
//         float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity * Time.deltaTime;

//         // --- 垂直旋转 (上下看) ---
//         xRotation -= mouseY;
//         xRotation = Mathf.Clamp(xRotation, -90f, 90f);
//         transform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);

//         // --- 水平旋转 (左右看) ---
//         playerBody.Rotate(Vector3.up * mouseX);
//     }

//     // --- 公共方法 ---

//     /// <summary>
//     /// 锁定鼠标并隐藏，允许玩家转动视角
//     /// </summary>
//     public void LockCursor()
//     {
//         Cursor.lockState = CursorLockMode.Locked;
//         Cursor.visible = false;
//         isCursorLocked = true;
//     }

//     /// <summary>
//     /// 解锁鼠标并显示，用于UI交互
//     /// </summary>
//     public void UnlockCursor()
//     {
//         Cursor.lockState = CursorLockMode.None;
//         Cursor.visible = true;
//         isCursorLocked = false;
//     }
// }
using UnityEngine;

public class MouseLook : MonoBehaviour
{
    // --- 单例模式 (保持不变) ---
    public static MouseLook Instance { get; private set; }

    // 增加对TouchLookInput脚本的引用
    [Header("Object References")]
    [SerializeField] private Transform playerBody;
    [SerializeField] private TouchLookInput touchInput; // 引用我们的触摸输入脚本

    [Header("Settings")]
    [SerializeField] private float lookSensitivity = 1.5f; // 为触摸调整一个新的灵敏度变量

    private float xRotation = 0f;
    private bool isLookEnabled = true; // 将isCursorLocked重命名为isLookEnabled，更符合触摸操作的语境

    private void Awake()
    {
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
        }
    }

    void Start()
    {
        // 在移动端，我们不需要处理光标的锁定和隐藏
        // 初始时允许视角转动
        LockCursor();
    }

    void Update()
    {
        // 只有当允许转动时才执行
        if (!isLookEnabled)
        {
            return;
        }

        // --- 从TouchLookInput获取输入，而不是鼠标 ---
        // 注意：touchInput.TouchDelta.x 对应 mouseX, touchInput.TouchDelta.y 对应 mouseY
        // 我们需要乘以一个合适的灵敏度，因为触摸的delta值范围和鼠标不同
        float lookX = touchInput.TouchDelta.x * lookSensitivity * Time.deltaTime;
        float lookY = touchInput.TouchDelta.y * lookSensitivity * Time.deltaTime;

        // --- 垂直旋转 (上下看) ---
        // 触摸操作的Y轴通常是反的，如果感觉不对，可以去掉这里的负号
        xRotation -= lookY;
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);
        transform.localRotation = Quaternion.Euler(xRotation, 0f, 0f);

        // --- 水平旋转 (左右看) ---
        playerBody.Rotate(Vector3.up * lookX);
    }

    // --- 公共方法 ---
    // 将方法重命名以更好地反映其功能

    /// <summary>
    /// 允许玩家转动视角
    /// </summary>
    public void LockCursor()
    {
        isLookEnabled = true;
        // 如果touchInput脚本被禁用了，也在这里启用它
        if(touchInput != null) touchInput.enabled = true;
    }

    /// <summary>
    /// 禁止玩家转动视角 (例如当打开UI菜单时)
    /// </summary>
    public void UnlockCursor()
    {
        isLookEnabled = false;
        // 禁用touchInput脚本以停止处理输入
        if(touchInput != null) touchInput.enabled = false;
    }
}